"""
    Created on 1 May 2014

    @author: Max Demian
"""


import re
import sys

from PyQt4 import QtGui, QtCore


class FileBrowser(QtGui.QWidget):

    def __init__(self):

        super(FileBrowser, self).__init__()

        # Main Window
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle("FileBrowser")
        self.setWindowIcon(QtGui.QIcon("data/icon.png"))

        QtGui.QToolTip.setFont(QtGui.QFont("SansSerif", 10))


def main():
    "Main entry point."

    app = QtGui.QApplication(sys.argv)
    c = FileBrowser()
    c.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
