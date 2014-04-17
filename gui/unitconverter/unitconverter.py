#!/usr/bin/env python2

import sys

from PyQt4 import QtGui
import conversion


class Converter(QtGui.QWidget):

    def __init__(self):
        super(Converter, self).__init__()

        self.initUI()

    def initUI(self):

        QtGui.QToolTip.setFont(QtGui.QFont("SansSerif", 10))

#         self.setToolTip("This is a <b>QWidget</b> widget")

        btn = QtGui.QPushButton("Button", self)
        btn.setToolTip("This is a <b>QPushButton</b> widget")
        btn.resize(btn.sizeHint())
#         btn.move(50, 50)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle("UnitConverter")
        self.setWindowIcon(QtGui.QIcon("data/calculator.png"))

        self.show()


def main():
    app = QtGui.QApplication(sys.argv)

    ex = Converter()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
