#!/usr/bin/env python2

import sys

from PyQt4 import QtGui, QtCore

from conversion import Data, Length, Volume


class Converter(QtGui.QMainWindow):

    def __init__(self):
        super(Converter, self).__init__()

        self.initUI()

    def initUI(self):

        QtGui.QToolTip.setFont(QtGui.QFont("SansSerif", 10))

        dbtn = QtGui.QPushButton("Quit", self)
        dbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        dbtn.resize(dbtn.sizeHint())
#         dbtn.move(0, 0)
        lbtn = QtGui.QPushButton("Quit", self)
        lbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        lbtn.resize(lbtn.sizeHint())
        lbtn.move(100, 0)
        vbtn = QtGui.QPushButton("Quit", self)
        vbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        vbtn.resize(vbtn.sizeHint())
        vbtn.move(200, 0)

        self.setGeometry(300, 300, 285, 150)
        self.setWindowTitle("UnitConverter")
        self.setWindowIcon(QtGui.QIcon("data/calculator.png"))

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main():
    app = QtGui.QApplication(sys.argv)

    c = Converter()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
