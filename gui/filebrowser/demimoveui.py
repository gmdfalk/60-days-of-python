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
import sys

from PyQt4 import QtGui, QtCore, uic

import fileops
import reporting


try:
    from docopt import docopt
except ImportError:
    print "ImportError: Please install docopt to use the CLI."


class PreviewFileModel(QtGui.QFileSystemModel):

    autopreview = False

    def columnCount(self, parent=QtCore.QModelIndex()):
        return super(PreviewFileModel, self).columnCount() + 1

    def data(self, index, role):
        if index.column() == self.columnCount() - 1:
            if role == QtCore.Qt.DisplayRole:
                return self.get_preview_text()
            if role == QtCore.Qt.TextAlignmentRole:
                return QtCore.Qt.AlignHCenter

        return super(PreviewFileModel, self).data(index, role)

    def get_preview_text(self, *args):
        return self.get_file_list()

    def get_file_list(self):
        return QtCore.QString("Preview here")

    def get_dir_list(self):
        pass


class DemiMoveGUI(QtGui.QMainWindow):

    def __init__(self, parent=None):

        super(DemiMoveGUI, self).__init__(parent)
        self.fileops = fileops.FileOps()
        uic.loadUi("demimove.ui", self)

        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.mainsplitter.setStretchFactor(0, 0)
        self.mainsplitter.setStretchFactor(1, 2)

        self.create_dirtree()
        self.create_browsertree()
        self.connect_buttons()
        log.info("demimove initialized.")

    def on_previewbutton(self):
        print self.sender()

    def on_refreshbutton(self):
        pass

    def on_renamebutton(self):
        pass

    def on_undobutton(self):
        pass

    def on_regexcheck(self, checked):
        if checked:
            pass

    def on_autopreviewcheck(self, checked):
        if checked:
            pass

    def on_extensioncheck(self, checked):
        if checked:
            self.fileops.keepext = True
        else:
            self.fileops.keepext = False
        print checked, self.fileops.keepext

    def on_hiddencheck(self, checked):
        if checked:
            pass

    def on_mirrorcheck(self, checked):
        if checked:
            pass

    def on_recursivecheck(self, checked):
        if checked:
            pass

    def on_autostopcheck(self, checked):
        if checked:
            pass
        # autosotp

    def insertpos(self, value):
        pass

    def insertedit(self, text):
        pass


    def on_replacecase(self):
        pass


    def on_replaceglob(self):
        pass


    def on_replaceregex(self):
        pass


    def on_insertpos(self):
        pass


    def on_insertedit(self):
        pass


    def on_countstart(self):
        pass


    def on_countstep(self):
        pass


    def on_countpreedit(self):
        pass


    def on_countsufedit(self):
        pass


    def on_countfillcheck(self):
        pass


    def on_removeduplicates(self):
        pass


    def on_removeextensions(self):
        pass


    def on_removewords(self):
        pass


    def on_varaccents(self):
        pass


    def connect_buttons(self):
        # Main buttons:
        self.previewbutton.clicked.connect(self.on_previewbutton)
        self.refreshbutton.clicked.connect(self.on_refreshbutton)
        self.renamebutton.clicked.connect(self.on_renamebutton)
        self.undobutton.clicked.connect(self.on_undobutton)
        # Main check and lineedits:
        self.regexcheck.clicked.connect(self.on_regexcheck)

        # Main options:
        self.autopreviewcheck.clicked.connect(self.on_autopreviewcheck)
        self.autostopcheck.clicked.connect(self.on_autostopcheck)
        self.extensioncheck.clicked.connect(self.on_extensioncheck)
        self.hiddencheck.clicked.connect(self.on_hiddencheck)
        self.mirrorcheck.clicked.connect(self.on_mirrorcheck)
        self.recursivecheck.clicked.connect(self.on_recursivecheck)

        # Replace options:
        self.replacecase.clicked.connect(self.on_replacecase)
        self.replaceglob.clicked.connect(self.on_replaceglob)
        self.replaceregex.clicked.connect(self.on_replaceregex)

        # Insert options:
        self.insertpos.valueChanged.connect(self.on_insertpos)
        self.insertedit.textChanged.connect(self.on_insertedit)

        # Count options:
        self.countstart.valueChanged.connect(self.on_countstart)
        self.countstep.valueChanged.connect(self.on_countstep)
        self.countpreedit.textChanged.connect(self.on_countpreedit)
        self.countsufedit.textChanged.connect(self.on_countsufedit)
        self.countfillcheck.clicked.connect(self.on_countfillcheck)

        # Remove options:
        self.removeduplicatescheck.clicked.connect(self.on_removeduplicates)
        self.removeextensionscheck.clicked.connect(self.on_removeextensions)
        self.removewordscheck.clicked.connect(self.on_removewords)

        # Various options:
        self.varaccentscheck.clicked.connect(self.on_varaccents)

    def create_dirtree(self):
        # Passing self as arg/parent here to avoid QTimer errors.
        self.dirmodel = QtGui.QFileSystemModel(self)
        self.dirmodel.setRootPath("")
        self.dirmodel.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.Hidden |
                                QtCore.QDir.NoDotAndDotDot)
        self.dirmodel.fileRenamed.connect(self.on_rootchange)
        self.dirmodel.rootPathChanged.connect(self.on_rootchange)
        self.dirmodel.directoryLoaded.connect(self.on_rootchange)

        self.dirtree.setModel(self.dirmodel)
        self.dirtree.setColumnHidden(1, True)
        self.dirtree.setColumnHidden(2, True)
        self.dirtree.setColumnHidden(3, True)

    def create_browsertree(self):
        self.browsermodel = PreviewFileModel(self)
        self.browsermodel.setRootPath("")
        self.browsermodel.setFilter(QtCore.QDir.Dirs | QtCore.QDir.Files |
                                    QtCore.QDir.NoDotAndDotDot |
                                    QtCore.QDir.Hidden)

        self.browsertree.setModel(self.browsermodel)
        self.browsertree.header().swapSections(4, 1)
        self.browsertree.setColumnHidden(2, True)

    def on_rootchange(self, *args):
#         print self.dirmodel.filePath(self.dirtree.currentIndex())
        path = self.dirmodel.filePath(self.dirtree.currentIndex())
#         print self.browsertree.selectionModel()
#         model = self.browsertree.model()
#         idx = model.index(model.rootPath())
#         for i in range(0, model.rowCount(idx)):
#             child = idx.child(i, idx.column())
#             print model.fileName(child)
#         print self.dirtree.currentIndex()
        print path
#         self.browsermodel.setRootPath(path)
#         self.browsertree.setRootIndex(self.dirtree.currentIndex())
#         self.browsertree.setRootIndex(self.dirmodel.index(path))

def main():
    "Main entry point for demimove."
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("demimove")
#     app.setStyle("plastique")
    gui = DemiMoveGUI()
    gui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    log = reporting.create_logger()

    try:
        args = docopt(__doc__, version="0.1")
        reporting.configure_logger(log, args["-v"], args["--quiet"])
    except NameError:
        reporting.configure_logger(log, loglevel=2, quiet=False)
        log.error("Please install docopt to use the CLI.")

    main()
