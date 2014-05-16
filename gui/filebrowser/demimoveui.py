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
        # Only set font to bold for the current working directory.
        if self.parent().cwdidx == index and self.parent().cwd:
            option.font.setWeight(QtGui.QFont.Bold)
        super(BoldDelegate, self).paint(painter, option, index)


class PreviewFileModel(QtGui.QFileSystemModel):

    _autopreview = True
    _cwd = ""
    _cwdidx = None

    def columnCount(self, parent=QtCore.QModelIndex()):
        return super(PreviewFileModel, self).columnCount() + 1

    def data(self, index, role):
        if index.column() == self.columnCount() - 1:
            if role == QtCore.Qt.DisplayRole:
                file_index = self.index(index.row(), 0, index.parent())
                entry = self.data(file_index, role)
                return self.get_preview(entry)

        return super(PreviewFileModel, self).data(index, role)

    def get_preview(self, item):
        if not self.autopreview:
            return QtCore.QString("")
#         if entry in ["demimove.py", "demimoveui.py", "fileops.pyc"]:
        return item.toString()

    @property
    def autopreview(self):
        return self._autopreview

    @autopreview.setter
    def autopreview(self, boolean):
        self._autopreview = boolean
        log.debug("autopreview: {}".format(boolean))


class DemiMoveGUI(QtGui.QMainWindow):

    def __init__(self, startdir, fileops, parent=None):

        super(DemiMoveGUI, self).__init__(parent)
        # Current working directory.
        self._cwd = ""
        self._cwdidx = None
        self.fileops = fileops
        uic.loadUi("demimove.ui", self)

        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.mainsplitter.setStretchFactor(0, 2)
        self.mainsplitter.setStretchFactor(1, 3)

        self.create_browser(startdir)
        self.connect_buttons()
        log.info("demimove-ui initialized.")

    def create_browser(self, startdir):
        self.browsermodel = PreviewFileModel(self)
        # TODO: With readOnly disabled we can use setData for renaming.
        self.browsermodel.setReadOnly(False)
        self.browsermodel.setRootPath("/")
        self.browsermodel.setFilter(QtCore.QDir.Dirs | QtCore.QDir.Files |
                                    QtCore.QDir.NoDotAndDotDot |
                                    QtCore.QDir.Hidden)

        self.browsermodel.dataChanged.connect(self.on_datachanged)
        self.browsermodel.fileRenamed.connect(self.on_filerenamed)

        self.browsertree.setModel(self.browsermodel)
        self.browsertree.setColumnHidden(2, True)
        self.browsertree.header().swapSections(4, 1)
        self.browsertree.header().resizeSection(0, 300)
        self.browsertree.header().resizeSection(4, 300)
        self.browsertree.setEditTriggers(QtGui.QAbstractItemView.EditKeyPressed)
#         self.browsertree.doubleClicked.connect(self.on_doubleclicked)
#         self.browsertree.selectionModel().currentChanged.connect(self.on_currentchanged)
        self.browsertree.setItemDelegate(BoldDelegate(self))

        index = self.browsermodel.index(startdir)
        self.browsertree.setCurrentIndex(index)
#         self.set_cwd()

    def set_cwd(self):
        "Set the current working directory for renaming actions."
        index = self.browsertree.currentIndex()
        path = self.browsermodel.filePath(index)
        if self.cwd and path == self.cwd:
            self.cwd = ""
            self.cwdidx = None
            return
        self.cwd = path
        self.cwdidx = index

    def keyPressEvent(self, e):
        "Connect return key to self.set_cwd()."
        if e.key() == QtCore.Qt.Key_Return:
            self.set_cwd()

    def on_datachanged(self):
        log.debug("dataChanged")

    @property
    def cwd(self):
        return self._cwd

    @cwd.setter
    def cwd(self, dir):
        if not os.path.isdir(dir) and not self._cwd:
            return
        self._cwd = dir
        self.browsermodel._cwd = dir
        log.debug("cwd: {}".format(self._cwd))
        if self._cwd:
            self.statusbar.showMessage("Root is now {}.".format(self._cwd))
        else:
            self.statusbar.showMessage("No root set.")

    @property
    def cwdidx(self):
        return self._cwdidx

    @cwdidx.setter
    def cwdidx(self, index):
        self._cwdidx = index
        self.browsermodel._cwdidx = index

    def on_doubleclicked(self):
        log.debug("doubleClicked")

    def on_dirloaded(self):
        log.debug("dirLoaded")

    def on_filerenamed(self):
        log.debug("fileRenamed")

    def on_rootchanged(self):
        log.debug("rootPathChanged")

    def on_rowsinserted(self):
        log.debug("rowsInserted")

    def on_currentchanged(self):
        log.debug("currentChanged")

    def connect_buttons(self):
        # Main buttons:
        self.previewbutton.clicked.connect(self.on_previewbutton)
        self.commitbutton.clicked.connect(self.on_commitbutton)
        self.undobutton.clicked.connect(self.on_undobutton)
        self.allradio.clicked.connect(self.on_allradio)
        self.dirsradio.clicked.connect(self.on_dirsradio)
        self.filesradio.clicked.connect(self.on_filesradio)

        # Main options:
        self.autopreviewcheck.clicked.connect(self.on_autopreviewcheck)
        self.autostopcheck.clicked.connect(self.on_autostopcheck)
        self.extensioncheck.clicked.connect(self.on_extensioncheck)
        self.hiddencheck.clicked.connect(self.on_hiddencheck)
        self.mirrorcheck.clicked.connect(self.on_mirrorcheck)
        self.recursivecheck.clicked.connect(self.on_recursivecheck)

        # Replace options:
        self.replacecheck.clicked.connect(self.on_replacecheck)
        self.replacecase.clicked.connect(self.on_replacecase)
        self.replaceglob.clicked.connect(self.on_replaceglob)
        self.replaceregex.clicked.connect(self.on_replaceregex)
        self.sourceedit.textChanged.connect(self.on_sourceedit)
        self.targetedit.textChanged.connect(self.on_targetedit)

        # Insert options:
        self.insertcheck.clicked.connect(self.on_insertcheck)
        self.insertpos.valueChanged.connect(self.on_insertpos)
        self.insertedit.textChanged.connect(self.on_insertedit)

        self.deletecheck.clicked.connect(self.on_deletecheck)
        self.deletestart.valueChanged.connect(self.on_deletestart)
        self.deleteend.valueChanged.connect(self.on_deleteend)

        # Count options:
        self.countcheck.clicked.connect(self.on_countcheck)
        self.countbase.valueChanged.connect(self.on_countbase)
        self.countpos.valueChanged.connect(self.on_countpos)
        self.countstep.valueChanged.connect(self.on_countstep)
        self.countpreedit.textChanged.connect(self.on_countpreedit)
        self.countsufedit.textChanged.connect(self.on_countsufedit)
        self.countfillcheck.clicked.connect(self.on_countfillcheck)

        # Remove options:
        self.removecheck.clicked.connect(self.on_removecheck)
        self.removeduplicatescheck.clicked.connect(self.on_removeduplicates)
        self.removeextensionscheck.clicked.connect(self.on_removeextensions)
        self.removenonwordscheck.clicked.connect(self.on_removenonwords)

        # Various options:
        self.varcheck.clicked.connect(self.on_varcheck)
        self.varaccentscheck.clicked.connect(self.on_varaccents)

        self.capitalizecheck.clicked.connect(self.on_capitalizecheck)
        self.capitalizebox.currentIndexChanged[int].connect(self.on_capitalbox)
        self.spacecheck.clicked.connect(self.on_capitalizecheck)
        self.spacebox.currentIndexChanged[int].connect(self.on_spacebox)

    def on_previewbutton(self):
        log.debug("{}".format(self.sender()))
#         self.fileops.stage(path)

    def on_commitbutton(self):
        print self.fileops.get_options()
        # self.fileops.commit()

    def on_undobutton(self):
        self.fileops.restore_options()
        # self.fileops.undo()

    def on_autopreviewcheck(self, checked):
        self.browsermodel.autopreview = checked
        self.browsertree.update()

    def on_extensioncheck(self, checked):
        self.fileops.keepext = checked

    def on_hiddencheck(self, checked):
        self.fileops.hidden = checked

    def on_mirrorcheck(self, checked):
        self.fileops.mirror = checked

    def on_recursivecheck(self, checked):
        self.fileops.recursive = checked

    def on_autostopcheck(self, checked):
        self.fileops.autostop = checked

    def on_replacecheck(self, checked):
        self.fileops.replacecheck = checked

    def on_replacecase(self, checked):
        self.fileops.ignorecase = not checked

    def on_replaceglob(self, checked):
        self.fileops.regex = not checked

    def on_replaceregex(self, checked):
        self.fileops.regex = checked

    def on_insertcheck(self, checked):
        self.fileops.insertcheck = checked

    def on_insertpos(self, num):
        self.fileops.insertpos = int(num)

    def on_insertedit(self, text):
        text = unicode(text).encode("utf-8")
        self.fileops.insertedit = text

    def on_countcheck(self, checked):
        self.fileops.countcheck = checked

    def on_countbase(self, num):
        self.fileops.countbase = int(num)

    def on_countpos(self, num):
        self.fileops.countpos = int(num)

    def on_countstep(self, num):
        self.fileops.countstep = int(num)

    def on_countpreedit(self, text):
        text = unicode(text).encode("utf-8")
        self.fileops.countpreedit = text

    def on_countsufedit(self, text):
        text = unicode(text).encode("utf-8")
        self.fileops.countsufedit = text

    def on_countfillcheck(self, checked):
        self.fileops.countfill = checked

    def on_removecheck(self, checked):
        self.fileops.removecheck = checked

    def on_removeduplicates(self, checked):
        self.fileops.remdups = checked

    def on_removeextensions(self, checked):
        self.fileops.remext = checked

    def on_removenonwords(self, checked):
        self.fileops.remnonwords = checked

    def on_varaccents(self, checked):
        self.fileops.accents = checked

    def on_allradio(self, checked):
        self.fileops.filesonly = False
        self.fileops.dirsonly = False
        self.browsermodel.setFilter(QtCore.QDir.Dirs | QtCore.QDir.Files |
                                    QtCore.QDir.NoDotAndDotDot |
                                    QtCore.QDir.Hidden)

    def on_dirsradio(self, checked):
        self.fileops.dirsonly = checked
        self.browsermodel.setFilter(QtCore.QDir.Dirs | QtCore.QDir.Hidden |
                                    QtCore.QDir.NoDotAndDotDot)

    def on_filesradio(self, checked):
        self.fileops.filesonly = checked
        self.browsermodel.setFilter(QtCore.QDir.Files | QtCore.QDir.Hidden |
                                    QtCore.QDir.NoDotAndDotDot)

    def on_capitalizecheck(self, checked):
        self.fileops.capitalizecheck = checked

    def on_sourceedit(self, text):
        text = unicode(text).encode("utf-8")
        self.fileops.sourceedit = text

    def on_targetedit(self, text):
        text = unicode(text).encode("utf-8")
        self.fileops.targetedit = text

    def on_deletecheck(self, checked):
        self.fileops.deletecheck = checked

    def on_deletestart(self, num):
        self.fileops.deletestart = int(num)

    def on_deleteend(self, num):
        self.fileops.deleteend = int(num)

    def on_varcheck(self, checked):
        self.fileops.varcheck = checked

    def on_capitalbox(self, index):
        self.fileops.capitalizemode = index

    def on_spacebox(self, index):
        self.fileops.spacemode = index


def main():
    "Main entry point for demimove-ui."
    startdir = os.getcwd()
    try:
        args = docopt(__doc__, version="0.1")
        args["-v"] = 3
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
