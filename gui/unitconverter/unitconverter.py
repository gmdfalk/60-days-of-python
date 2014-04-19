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

        grid = QtGui.QGridLayout()

        labels = [0, "bits", 0, "bytes", 0, "KB", 0, "KiB", 0, "MB", 0, "MiB",
                  0, "GB", 0, "GiB", 0, "TB", 0, "TiB", 0, "PB", 0, "PiB"]
        pos = [(0, 0), (0, 1), (0, 2), (0, 3),
               (1, 0), (1, 1), (1, 2), (1, 3),
               (2, 0), (2, 1), (2, 2), (2, 3),
               (3, 0), (3, 1), (3, 2), (3, 3),
               (4, 0), (4, 1), (4, 2), (4, 3),
               (5, 0), (5, 1), (5, 2), (5, 3)]

        for i in range(len(labels)):
            if labels[i]:
                grid.addWidget(QtGui.QLabel(labels[i]), pos[i][0], pos[i][1])
            else:
                grid.addWidget(QtGui.QLineEdit(self), pos[i][0], pos[i][1])

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
        # ~
        # ~ self.bitlabel = QtGui.QLabel(self)
        # ~ self.bitfield = QtGui.QLineEdit(self)
        # ~ self.bitfield.move(0, 60)
        # ~ self.bitlabel.move(130, 60)
        # ~ self.bitlabel.setText("bits")
# ~
        # ~ self.KBlabel = QtGui.QLabel(self)
        # ~ self.KBfield = QtGui.QLineEdit(self)
        # ~ self.KBfield.move(0, 90)
        # ~ self.KBlabel.move(130, 90)
        # ~ self.KBlabel.setText("KB")
# ~
        # ~ self.MBlabel = QtGui.QLabel(self)
        # ~ self.MBfield = QtGui.QLineEdit(self)
        # ~ self.MBfield.move(0, 120)
        # ~ self.MBlabel.move(130, 120)
        # ~ self.MBlabel.setText("MB")
        # ~ self.MBfield.textChanged[str].connect(self.megabytes_changed)
        # ~ self.MBfield.textChanged[str].connect(self.update_data)
# ~
        # ~ self.GBlabel = QtGui.QLabel(self)
        # ~ self.GBfield = QtGui.QLineEdit(self)
        # ~ self.GBfield.move(0, 150)
        # ~ self.GBlabel.move(130, 150)
        # ~ self.GBlabel.setText("GB")
# ~
        # ~ self.TBlabel = QtGui.QLabel(self)
        # ~ self.TBfield = QtGui.QLineEdit(self)
        # ~ self.TBfield.move(0, 180)
        # ~ self.TBlabel.move(130, 180)
        # ~ self.TBlabel.setText("TB")
# ~
        # ~ self.PBlabel = QtGui.QLabel(self)
        # ~ self.PBfield = QtGui.QLineEdit(self)
        # ~ self.PBfield.move(0, 210)
        # ~ self.PBlabel.move(130, 210)
        # ~ self.PBlabel.setText("PB")
# ~
        # ~ self.byteslabel = QtGui.QLabel(self)
        # ~ self.bytesfield = QtGui.QLineEdit(self)
        # ~ self.bytesfield.move(180, 60)
        # ~ self.byteslabel.move(310, 60)
        # ~ self.byteslabel.setText("bytes")
# ~
        # ~ self.KiBlabel = QtGui.QLabel(self)
        # ~ self.KiBfield = QtGui.QLineEdit(self)
        # ~ self.KiBfield.move(180, 90)
        # ~ self.KiBlabel.move(310, 90)
        # ~ self.KiBlabel.setText("KiB")
# ~
        # ~ self.MiBlabel = QtGui.QLabel(self)
        # ~ self.MiBfield = QtGui.QLineEdit(self)
        # ~ self.MiBfield.move(180, 120)
        # ~ self.MiBlabel.move(310, 120)
        # ~ self.MiBlabel.setText("MiB")
# ~
        # ~ self.GiBlabel = QtGui.QLabel(self)
        # ~ self.GiBfield = QtGui.QLineEdit(self)
        # ~ self.GiBfield.move(180, 150)
        # ~ self.GiBlabel.move(310, 150)
        # ~ self.GiBlabel.setText("GiB")
# ~
        # ~ self.TiBlabel = QtGui.QLabel(self)
        # ~ self.TiBfield = QtGui.QLineEdit(self)
        # ~ self.TiBfield.move(180, 180)
        # ~ self.TiBlabel.move(310, 180)
        # ~ self.TiBlabel.setText("TiB")
# ~
        # ~ self.PiBlabel = QtGui.QLabel(self)
        # ~ self.PiBfield = QtGui.QLineEdit(self)
        # ~ self.PiBfield.move(180, 210)
        # ~ self.PiBlabel.move(310, 210)
        # ~ self.PiBlabel.setText("PiB")


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
