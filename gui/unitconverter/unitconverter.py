#!/usr/bin/env python2

import sys

from PyQt4 import Qt, QtGui, QtCore

from conversion import Data, Length, Volume


class Converter(QtGui.QWidget):

    def __init__(self, app):
        super(Converter, self).__init__()
        self.app = app
        self.initUI()

    def initUI(self):

        QtGui.QToolTip.setFont(QtGui.QFont("SansSerif", 10))

        self.create_buttons()

        self.data = Data()
        self.create_data_fields()

        # Main Window
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle("UnitConverter")
        self.setWindowIcon(QtGui.QIcon("data/calculator.png"))

        self.show()

    def create_buttons(self):
#         "Creates the buttons at the top."
#         dbtn = QtGui.QPushButton("Data", self)
#         dbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
#
#         lbtn = QtGui.QPushButton("Length", self)
#         vbtn = QtGui.QPushButton("Volume", self)
#         nbtn = QtGui.QPushButton("Numbers", self)
#
#         hbox = QtGui.QHBoxLayout()
#         hbox.addStretch(1)
#         hbox.addWidget(dbtn)
#         hbox.addWidget(lbtn)
#         hbox.addWidget(vbtn)
#         hbox.addWidget(nbtn)
#
#         vbox = QtGui.QVBoxLayout()
#         vbox.addStretch(1)
#         vbox.addLayout(hbox)
#
#         self.setLayout(vbox)
        pass

    def clear_gui(self):
        "Delete elements so we can switch to a different conversion mode."
        for widget in self.app.allWidgets():
            if isinstance(widget, QtGui.QLineEdit):
                widget.deleteLater()
            if isinstance(widget, QtGui.QLabel):
                widget.deleteLater()

    def create_data_fields(self):

        self.bits = QtGui.QLineEdit()
        self.bytes = QtGui.QLineEdit()
        self.KB = QtGui.QLineEdit()
        self.KiB = QtGui.QLineEdit()
        self.MB = QtGui.QLineEdit()
        self.MiB = QtGui.QLineEdit()
        self.GB = QtGui.QLineEdit()
        self.GiB = QtGui.QLineEdit()
        self.TB = QtGui.QLineEdit()
        self.TiB = QtGui.QLineEdit()
        self.PB = QtGui.QLineEdit()
        self.PiB = QtGui.QLineEdit()

        data = [self.bits, "bits", self.bytes, "bytes", self.KB, "KB",
                self.KiB, "KiB", self.MB, "MB", self.MiB, "MiB",
                self.GB, "GB", self.GiB, "GiB", self.TB, "TB",
                self.TiB, "TiB", self.PB, "PB", self.PiB, "PiB"]

        pos = [(0, 0), (0, 1), (0, 2), (0, 3),
               (1, 0), (1, 1), (1, 2), (1, 3),
               (2, 0), (2, 1), (2, 2), (2, 3),
               (3, 0), (3, 1), (3, 2), (3, 3),
               (4, 0), (4, 1), (4, 2), (4, 3),
               (5, 0), (5, 1), (5, 2), (5, 3)]

        # Create the grid layout from our lists.
        grid = QtGui.QGridLayout()

        for i in range(len(data)):
            if isinstance(data[i], str):
                grid.addWidget(QtGui.QLabel(data[i]), pos[i][0], pos[i][1])
            else:
                print i
                grid.addWidget(data[i], pos[i][0], pos[i][1])

#         dbtn = QtGui.QPushButton("Data", self)
#         dbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
#         lbtn = QtGui.QPushButton("Length", self)
#         vbtn = QtGui.QPushButton("Volume", self)
#         nbtn = QtGui.QPushButton("Numbers", self)

        grid.addWidget(QtGui.QPushButton("Data", self), 6, 0)
        grid.addWidget(QtGui.QPushButton("Volume", self), 6, 2)
        grid.addWidget(QtGui.QPushButton("Length", self), 7, 0)
        grid.addWidget(QtGui.QPushButton("Numbers", self), 7, 2)
#         hbox = QtGui.QHBoxLayout()
#         hbox.addStretch(1)
#         hbox.addWidget(dbtn)
#         hbox.addWidget(lbtn)
#         hbox.addWidget(vbtn)
#         hbox.addWidget(nbtn)
#
#         vbox = QtGui.QVBoxLayout()
#         vbox.addStretch(1)
#         vbox.addLayout(hbox)
        self.setLayout(grid)

    def precision_changed(self, text):
        self.data.precision = int(text)

    def update_data(self):
        self.bitfield.setText(str(self.data.bits))
        self.bytesfield.setText(str(self.data.bytes))
        self.KBfield.setText(str(self.data.kilobytes))
        self.KiBfield.setText(str(self.data.kibibytes))
#         self.MBfield.setText(str(self.data.megabytes))
        self.MiBfield.setText(str(self.data.mebibytes))
        self.GBfield.setText(str(self.data.gigabytes))
        self.GiBfield.setText(str(self.data.gibibytes))
        self.TBfield.setText(str(self.data.terrabytes))
        self.TiBfield.setText(str(self.data.tebibytes))
        self.PBfield.setText(str(self.data.petabytes))
        self.PiBfield.setText(str(self.data.pebibytes))

    def megabytes_changed(self, text):

        try:
            self.data.megabytes = float(text)
        except ValueError:
            self.data.megabytes = 0


def main():
    app = QtGui.QApplication(sys.argv)

    c = Converter(app)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
