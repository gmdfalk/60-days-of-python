import re
import sys

from PyQt4 import QtGui, QtCore, uic


class MassRenamer(QtGui.QMainWindow):

    def __init__(self, parent=None):

        super(MassRenamer, self).__init__(parent)
        uic.loadUi("filebrowser.ui", self)

#         print self.mainsplitter.sizes()
        self.mainsplitter.setStretchFactor(0, 1)
        self.mainsplitter.setStretchFactor(1, 30)
#         print self.mainsplitter.sizes()

        self.setWindowIcon(QtGui.QIcon("icon.png"))

        self.create_dirtree()
        self.create_browsertree()

    def create_dirtree(self):
        self.dirmodel = QtGui.QFileSystemModel()
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
        self.browsermodel = QtGui.QFileSystemModel()
        self.browsermodel.setRootPath("")
        self.browsermodel.setFilter(QtCore.QDir.Dirs | QtCore.QDir.Files |
                                    QtCore.QDir.NoDotAndDotDot |
                                    QtCore.QDir.Hidden)

        self.browsertree.setModel(self.browsermodel)

    def on_rootchange(self, *args):
        print self.sender()


def main():
    "Main entry point."

    app = QtGui.QApplication(sys.argv)
    browser = MassRenamer()
    browser.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
