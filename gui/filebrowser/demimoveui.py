"""demimove-ui

Usage:
    dmv-ui [-d <dir>] [-c <file>] [-v...] [-q] [-h]

Options:
    -c, --config=<file>  Specify a config file to load.
    -d, --dir=<dir>      Specify a directory to load.
    -v                   Logging verbosity level, up to -vvv.
    -q, --quiet          Do not print logging messages to console.
    -h,  --help          Show this help text and exit.
    --version            Show the current demimove-ui version.
"""
# TODO: ConfigParser
import os
import random
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
        uic.loadUi("demimove.ui", self)

        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.mainsplitter.setStretchFactor(0, 0)
        self.mainsplitter.setStretchFactor(1, 2)

        self.create_dirtree()
        self.create_browsertree()
        log.info("demimove initialized.")

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
