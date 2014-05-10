import re
import sys

from PyQt4 import QtGui, QtCore, uic


class MassRenamer(QtGui.QMainWindow):

    def __init__(self, parent=None):

        super(MassRenamer, self).__init__(parent)
        uic.loadUi("filebrowser.ui", self)

        self.setWindowTitle("MassRenamer")
        self.setWindowIcon(QtGui.QIcon("icon.png"))

        model = QtGui.QFileSystemModel()
        model.setRootPath("")
        model.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.NoDotAndDotDot |
                        QtCore.QDir.Hidden)

        self.dirtree.setModel(model)
        self.dirtree.setColumnHidden(1, True)
        self.dirtree.setColumnHidden(2, True)
        self.dirtree.setColumnHidden(3, True)
        self.dirtree.header().hide()


def main():
    "Main entry point."

    app = QtGui.QApplication(sys.argv)
    browser = MassRenamer()
    browser.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
