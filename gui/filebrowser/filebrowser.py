"""
    Created on 1 May 2014

    @author: Max Demian
"""


import re
import sys

from PyQt4 import QtGui, QtCore, uic


class FileBrowser(QtGui.QMainWindow):

    def __init__(self, parent=None):

        super(FileBrowser, self).__init__(parent)
        uic.loadUi("filebrowser.ui", self)
        # Main Window
#         self.setGeometry(300, 200, 760, 600)
#         self.setWindowTitle("FileBrowser")
#         self.setWindowIcon(QtGui.QIcon("data/icon.png"))
#
#         QtGui.QToolTip.setFont(QtGui.QFont("SansSerif", 10))
#
#         model = QtGui.QFileSystemModel()
#         model.setRootPath("")
#         model.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.NoDotAndDotDot |
#                         QtCore.QDir.Hidden)
#         view = QtGui.QTreeView()
#         view.setModel(model)
#         view.setColumnHidden(1, True)
#         view.setColumnHidden(2, True)
#         view.setColumnHidden(3, True)
#         view.header().hide()
#         self.setCentralWidget(view)


def main():
    "Main entry point."

    app = QtGui.QApplication(sys.argv)
    browser = FileBrowser()
    browser.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
