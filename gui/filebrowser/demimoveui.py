# encoding: utf-8
"""demimove-ui

Usage:
    dmv-ui [-d <path>] [-c <file>] [-v|-vv|-vvv] [-q] [-h]

Options:
    -c, --config=<file>  <NYI> Specify a config file to load.
    -d, --dir=<path>     Specify the working directory. Otherwise CWD is used.
    -v                   Logging verbosity level, up to -vvv.
    -q, --quiet          Do not print logging messages to console.
    -h,  --help          Show this help text and exit.
    --version            Show the current demimove-ui version.
"""
# TODO: ConfigParser
# TODO: Custom ContextMenu for Filebrowser
# FIXME: Switching between dirs/files/both destroys CWD marker.
#        Fixed temporariliy by commenting filter changes.
import logging
import sys

from PyQt4 import QtGui, QtCore, uic

from fileops import FileOps
import os


log = logging.getLogger("gui")

try:
    from docopt import docopt
except ImportError:
    print "ImportError: Please install docopt to use the CLI."


class BoldDelegate(QtGui.QStyledItemDelegate):

    def paint(self, painter, option, index):
        if self.parent().cwdidx == index:
            option.font.setWeight(QtGui.QFont.Bold)
        super(BoldDelegate, self).paint(painter, option, index)


class StatusTableModel (QtCore.QAbstractTableModel):
    "Placeholder for status messages."
    def __init__(self, data, header, parent=None, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.data = data
        self.header = header

    def flags(self, index):
        return (QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable |
                QtCore.Qt.ItemIsSelectable)

    def rowCount(self, parent):
        return len(self.data)

    def columnCount(self, parent):
        return 2

    def setData(self, index, value, role):
        if index.isValid() and role == QtCore.Qt.CheckStateRole:
            if value == QtCore.Qt.Checked:
                self.data[index.row()].setChecked(True)
            else:
                self.data[index.row()].setChecked(False)

        self.dataChanged.emit(index, index)
        return True

    def data(self, index, role):
        if index.isValid():
            if role == QtCore.Qt.CheckStateRole:
                if self.data[index.row()].isChecked():
                    return QtCore.QVariant(QtCore.Qt.Checked)
                else:
                    return QtCore.QVariant(QtCore.Qt.Unchecked)
            elif role == QtCore.Qt.FontRole:
                font = QtGui.QFont()
                if self.data[index.row()].isChecked():
                    font.setBold(True)
                else:
                    font.setBold(False)
                return QtCore.QVariant(font)
            elif role == QtCore.Qt.DisplayRole:
                return QtCore.QVariant(self.data[index.row()].text())

        return QtCore.QVariant()

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.header)
        return QtCore.QVariant()


class PreviewFileModel(QtGui.QFileSystemModel):

    def __init__(self, parent=None):
        super(PreviewFileModel, self).__init__(parent)
        self.p = parent
        self._cwd = ""
        self._cwdidx = None
        self._sourceedit = None
        self._targetedit = None
        self._mediamode = None

    def columnCount(self, parent=QtCore.QModelIndex()):
        return super(PreviewFileModel, self).columnCount() + 1

    def data(self, index, role):
        if index.column() == self.columnCount() - 1:
            if role == QtCore.Qt.DisplayRole:
                fileindex = self.index(index.row(), 0, index.parent())
                item = self.data(fileindex, role)
                return self.update_preview(item, fileindex)

        return super(PreviewFileModel, self).data(index, role)

    def update_preview(self, item, index):
        if self.p.autopreview:
            if not self._cwdidx:
                return
            return self.match_preview_alt(item, index)

    def match_preview(self, item, index):
        par, cidx = index.parent(), self._cwdidx
        parents = [par]
        if self.p.fileops.recursive:
            for i in xrange(16):
                par = par.parent()
                parents.append(par)
        if cidx in parents:
            if item.toString() in self.p.targetlist:
                idx = self.p.targetlist.index(item.toString())
                return self.p.previewlist[idx]

    def match_preview_alt(self, item, index):
        d = self.filePath(index)
        if self._cwd in d and item.toString() in self.p.targetlist:
            idx = self.p.targetlist.index(item.toString())
            return self.p.previewlist[idx]


class DemiMoveGUI(QtGui.QMainWindow):

    def __init__(self, startdir, fileops, parent=None):

        super(DemiMoveGUI, self).__init__(parent)
        # Current working directory.
        self._autopreview = True
        self._cwd = ""
        self._cwdidx = None
        self._sourceedit = ""  # Pattern to search for in files/dirs.
        self._targetedit = ""  # Pattern to replace above found matches with.
        self.targetlist = []
        self.fileops = fileops
        uic.loadUi("demimove.ui", self)

        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.mainsplitter.setStretchFactor(0, 2)
        self.mainsplitter.setStretchFactor(1, 3)

        self.checks = [self.capitalizecheck, self.spacecheck, self.removecheck,
                       self.varaccentscheck, self.removeduplicatescheck,
                       self.autopreviewcheck, self.extensioncheck,
                       self.removenonwordscheck, self.removeextensionscheck, ]
        self.boxes = [self.capitalizebox, self.spacebox]

        self.create_browser(startdir)
        self.create_statustab()
        self.create_historytab()
        self.connect_buttons()
        log.info("demimove-ui initialized.")
        self.statusbar.showMessage("Select a directory and press Enter.")

    def create_browser(self, startdir):
        self.dirmodel = PreviewFileModel(self)
        # TODO: With readOnly disabled we can use setData for renaming.
        self.dirmodel.setReadOnly(False)
        self.dirmodel.setRootPath("/")
        self.dirmodel.setFilter(QtCore.QDir.Dirs | QtCore.QDir.Files |
                                    QtCore.QDir.NoDotAndDotDot |
                                    QtCore.QDir.Hidden)

        self.dirtree.setModel(self.dirmodel)
        self.dirtree.setColumnHidden(2, True)
        self.dirtree.header().swapSections(4, 1)
        self.dirtree.header().resizeSection(0, 300)
        self.dirtree.header().resizeSection(4, 300)
        self.dirtree.setEditTriggers(QtGui.QAbstractItemView.EditKeyPressed)
        self.dirtree.setItemDelegate(BoldDelegate(self))

        index = self.dirmodel.index(startdir)
        self.dirtree.setCurrentIndex(index)

    def create_statustab(self):
        header = "Checkboxes"
        data = [QtGui.QCheckBox("item 1"),
                QtGui.QCheckBox("item 2"),
                QtGui.QCheckBox("item 3"),
                QtGui.QCheckBox("item 4"),
                QtGui.QCheckBox("item 5")]

        model = StatusTableModel(data, header, self)
        self.statustable.setModel(model)


    def create_historytab(self):
        pass

    def set_cwd(self):
        "Set the current working directory for renaming actions."
        index = self.dirtree.currentIndex()
        path = self.dirmodel.filePath(index)
        if self.cwd and path == self.cwd:
            self.dirtree.setExpanded(self.cwdidx, False)
            self.cwd = ""
            self.cwdidx = None
        elif path != self.cwd and os.path.isdir(path):
            self.cwd = path
            self.cwdidx = index
            self.dirtree.setExpanded(self.cwdidx, True)
        self.update_single_index(index)

    def keyPressEvent(self, e):
        "Overloaded to connect return key to self.set_cwd()."
        if e.key() == QtCore.Qt.Key_Return:
            self.set_cwd()
            if self.cwd:
                self.update_lists()

    def update_lists(self):
        trgts, prvws = self.fileops.stage(str(self.cwd))
        self.targetlist = [i[1] + i[2] if len(i) > 2 else i[1] for i in trgts]
        self.previewlist = [i[1] + i[2] if len(i) > 2 else i[1] for i in prvws]
#         log.debug(self.targetlist)
#         log.debug(self.previewlist)
        self.update_view()

    def update_view(self):
        m, v = self.dirmodel, self.dirtree
        r = v.rect()
        m.dataChanged.emit(v.indexAt(r.topLeft()), v.indexAt(r.bottomRight()))

    def update_single_index(self, index):
        m = self.dirmodel
        m.dataChanged.emit(index, m.index(index.row(), m.columnCount()))

    def connect_buttons(self):
        # Main buttons:
        self.commitbutton.clicked.connect(self.on_commitbutton)
        self.undobutton.clicked.connect(self.on_undobutton)
        self.allradio.toggled.connect(self.on_allradio)
        self.dirsradio.toggled.connect(self.on_dirsradio)
        self.filesradio.toggled.connect(self.on_filesradio)

        # Main options:
        self.autopreviewcheck.toggled.connect(self.on_autopreviewcheck)
        self.autostopcheck.toggled.connect(self.on_autostopcheck)
        self.extensioncheck.toggled.connect(self.on_extensioncheck)
        self.hiddencheck.toggled.connect(self.on_hiddencheck)
        self.mirrorcheck.toggled.connect(self.on_mirrorcheck)
        self.recursivecheck.toggled.connect(self.on_recursivecheck)

        # Replace options:
        self.replacecheck.toggled.connect(self.on_replacecheck)
        self.replacecase.toggled.connect(self.on_replacecase)
        self.replaceglob.toggled.connect(self.on_replaceglob)
        self.replacematchonly.toggled.connect(self.on_replacematchonly)
        self.replaceregex.toggled.connect(self.on_replaceregex)
        self.sourceedit.textChanged.connect(self.on_sourceedit)
        self.targetedit.textChanged.connect(self.on_targetedit)

        # Insert options:
        self.insertcheck.toggled.connect(self.on_insertcheck)
        self.insertpos.valueChanged.connect(self.on_insertpos)
        self.insertedit.textChanged.connect(self.on_insertedit)

        self.deletecheck.toggled.connect(self.on_deletecheck)
        self.deletestart.valueChanged.connect(self.on_deletestart)
        self.deleteend.valueChanged.connect(self.on_deleteend)

        # Count options:
        self.countcheck.toggled.connect(self.on_countcheck)
        self.countbase.valueChanged.connect(self.on_countbase)
        self.countpos.valueChanged.connect(self.on_countpos)
        self.countstep.valueChanged.connect(self.on_countstep)
        self.countpreedit.textChanged.connect(self.on_countpreedit)
        self.countsufedit.textChanged.connect(self.on_countsufedit)
        self.countfillcheck.toggled.connect(self.on_countfillcheck)

        # Remove options:
        self.removecheck.toggled.connect(self.on_removecheck)
        self.removeduplicatescheck.toggled.connect(self.on_removeduplicates)
        self.removeextensionscheck.toggled.connect(self.on_removeextensions)
        self.removenonwordscheck.toggled.connect(self.on_removenonwords)

        # Various options:
        self.varcheck.toggled.connect(self.on_varcheck)
        self.varaccentscheck.toggled.connect(self.on_varaccents)
        self.varmediacheck.toggled.connect(self.on_varmediacheck)

        self.capitalizecheck.toggled.connect(self.on_capitalizecheck)
        self.capitalizebox.currentIndexChanged[int].connect(self.on_capitalbox)
        self.spacecheck.toggled.connect(self.on_spacecheck)
        self.spacebox.currentIndexChanged[int].connect(self.on_spacebox)

    def on_commitbutton(self):
        self.update_lists()
        log.debug(self.fileops.get_options())
#         self.fileops.commit()

    def on_undobutton(self):
        self.fileops.undo()

    def on_autopreviewcheck(self, checked):
        self.autopreview = checked
        if checked:
            self.update_lists()

    def on_extensioncheck(self, checked):
        self.fileops.keepext = checked
        if self.autopreview:
            self.update_lists()

    def on_hiddencheck(self, checked):
        self.fileops.hidden = checked
        if self.autopreview:
            self.update_lists()

    def on_mirrorcheck(self, checked):
        self.fileops.mirror = checked
        if self.autopreview:
            self.update_lists()

    def on_recursivecheck(self, checked):
        self.fileops.recursive = checked
        if self.autopreview:
            self.update_lists()

    def on_autostopcheck(self, checked):
        self.fileops.autostop = checked

    def on_replacecheck(self, checked):
        self.fileops.replacecheck = checked
        if self.autopreview:
            self.update_lists()

    def on_replacecase(self, checked):
        self.fileops.ignorecase = checked
        if self.autopreview:
            self.update_lists()

    def on_replacematchonly(self, checked):
        self.fileops.matchonly = checked
        if self.autopreview:
            self.update_lists()

    def on_replaceglob(self, checked):
        self.fileops.regex = not checked
        if self.autopreview:
            self.update_lists()

    def on_replaceregex(self, checked):
        self.fileops.regex = checked
        if self.autopreview:
            self.update_lists()

    def on_insertcheck(self, checked):
        self.fileops.insertcheck = checked
        if self.autopreview:
            self.update_lists()

    def on_insertpos(self, num):
        self.fileops.insertpos = int(num)
        if self.autopreview:
            self.update_lists()

    def on_insertedit(self, text):
        text = unicode(text).encode("utf-8")
        self.fileops.insertedit = text
        if self.autopreview:
            self.update_lists()

    def on_countcheck(self, checked):
        self.fileops.countcheck = checked
        if self.autopreview:
            self.update_lists()

    def on_countbase(self, num):
        self.fileops.countbase = int(num)
        if self.autopreview:
            self.update_lists()

    def on_countpos(self, num):
        self.fileops.countpos = int(num)
        if self.autopreview:
            self.update_lists()

    def on_countstep(self, num):
        self.fileops.countstep = int(num)
        if self.autopreview:
            self.update_lists()

    def on_countpreedit(self, text):
        text = unicode(text).encode("utf-8")
        self.fileops.countpreedit = text
        if self.autopreview:
            self.update_lists()

    def on_countsufedit(self, text):
        text = unicode(text).encode("utf-8")
        self.fileops.countsufedit = text
        if self.autopreview:
            self.update_lists()

    def on_countfillcheck(self, checked):
        self.fileops.countfill = checked
        if self.autopreview:
            self.update_lists()

    def on_removecheck(self, checked):
        self.fileops.removecheck = checked
        if self.autopreview:
            self.update_lists()

    def on_removeduplicates(self, checked):
        self.fileops.remdups = checked
        if self.autopreview:
            self.update_lists()

    def on_removeextensions(self, checked):
        self.fileops.remext = checked
        if self.autopreview:
            self.update_lists()

    def on_removenonwords(self, checked):
        self.fileops.remnonwords = checked
        if self.autopreview:
            self.update_lists()

    def on_varaccents(self, checked):
        self.fileops.accents = checked
        if self.autopreview:
            self.update_lists()

    def save_options(self):
        self.checksaves = {i: i.isChecked() for i in self.checks}
        self.combosaves = {i: i.currentIndex() for i in self.boxes}

    def restore_options(self):
        for k, v in self.checksaves.items():
            k.setChecked(v)
        for k, v in self.combosaves.items():
            k.setCurrentIndex(v)

    def set_mediaoptions(self):
        for i in self.checks[:-2]:
            i.setChecked(True)
        self.spacebox.setCurrentIndex(6)
        self.capitalizebox.setCurrentIndex(0)

    def toggle_options(self, boolean):
        if boolean:
            self.save_options()
            self.set_mediaoptions()
        else:
            self.restore_options()

    def on_varmediacheck(self, checked):
        self.toggle_options(checked)
        if self.autopreview:
            self.update_lists()

    def on_allradio(self, checked):
        self.fileops.filesonly = False
        self.fileops.dirsonly = False
#         self.dirmodel.setFilter(QtCore.QDir.Dirs | QtCore.QDir.Files |
#                                     QtCore.QDir.NoDotAndDotDot |
#                                     QtCore.QDir.Hidden)
        if self.autopreview:
            self.update_lists()

    def on_dirsradio(self, checked):
        self.fileops.dirsonly = checked
#         self.dirmodel.setFilter(QtCore.QDir.Dirs | QtCore.QDir.Hidden |
#                                     QtCore.QDir.NoDotAndDotDot)
        if self.autopreview:
            self.update_lists()

    def on_filesradio(self, checked):
        self.fileops.filesonly = checked
#         self.dirmodel.setFilter(QtCore.QDir.Files | QtCore.QDir.Hidden |
#                                     QtCore.QDir.NoDotAndDotDot)
        if self.autopreview:
            self.update_lists()

    def on_spacecheck(self, checked):
        self.fileops.spacecheck = checked
        if self.autopreview:
            self.update_lists()

    def on_capitalizecheck(self, checked):
        self.fileops.capitalizecheck = checked
        if self.autopreview:
            self.update_lists()

    def on_sourceedit(self, text):
        text = unicode(text).encode("utf-8")
        self.sourceedit = text
        if self.autopreview:
            self.update_lists()

    def on_targetedit(self, text):
        text = unicode(text).encode("utf-8")
        self.targetedit = text
        if self.autopreview:
            self.update_lists()

    def on_deletecheck(self, checked):
        self.fileops.deletecheck = checked
        if self.autopreview:
            self.update_lists()

    def on_deletestart(self, num):
        self.fileops.deletestart = int(num)
        if self.autopreview:
            self.update_lists()

    def on_deleteend(self, num):
        self.fileops.deleteend = int(num)
        if self.autopreview:
            self.update_lists()

    def on_varcheck(self, checked):
        self.fileops.varcheck = checked
        if self.autopreview:
            self.update_lists()

    def on_capitalbox(self, index):
        self.fileops.capitalizemode = index
        if self.autopreview:
            self.update_lists()

    def on_spacebox(self, index):
        self.fileops.spacemode = index
        if self.autopreview:
            self.update_lists()

    @property
    def cwd(self):
        return self._cwd

    @cwd.setter
    def cwd(self, path):
        # Exit out if dir is not a valid target.
        self._cwd = path
        self.dirmodel._cwd = path
        log.debug("cwd: {}".format(self._cwd))
        if self._cwd:
            self.statusbar.showMessage("Root is now {}.".format(self._cwd))
        else:
            self.statusbar.showMessage("No root set.")

    @property
    def mediamode(self):
        return self._mediamode

    @mediamode.setter
    def mediamode(self, boolean):
        self._mediamode = boolean
        log.debug("mediamode: {}".format(boolean))

    @property
    def autopreview(self):
        return self._autopreview

    @autopreview.setter
    def autopreview(self, boolean):
        self._autopreview = boolean
        log.debug("autopreview: {}".format(boolean))

    @property
    def cwdidx(self):
        return self._cwdidx

    @cwdidx.setter
    def cwdidx(self, index):
        self._cwdidx = index
        self.dirmodel._cwdidx = index

    @property
    def sourceedit(self):
        return self._sourceedit

    @sourceedit.setter
    def sourceedit(self, text):
        log.debug("sourceedit: {}.".format(text))
        self._sourceedit = text

    @property
    def targetedit(self):
        return self._targetedit

    @targetedit.setter
    def targetedit(self, text):
        log.debug("targetedit: {}.".format(text))
        self._targetedit = text


def main():
    "Main entry point for demimove-ui."
    startdir = os.getcwd()
    try:
        args = docopt(__doc__, version="0.1")
        args["-v"] = 3  # Force debug mode, for now.
        fileops = FileOps(verbosity=args["-v"], quiet=args["--quiet"])
        if args["--dir"]:
            startdir = args["--dir"]
    except NameError:
        fileops = fileops.FileOps()
        log.error("Please install docopt to use the CLI.")

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("demimove-ui")
#     app.setStyle("plastique")
    gui = DemiMoveGUI(startdir, fileops)
    gui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
