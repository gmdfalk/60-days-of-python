#!/usr/bin/env python2

from threading import Timer
import sys

from PyQt4 import QtGui, QtCore

from conversion import Data, Length, Volume


class Converter(QtGui.QWidget):

    def __init__(self):
        super(Converter, self).__init__()

        self.initUI()

    def initUI(self):

        QtGui.QToolTip.setFont(QtGui.QFont("SansSerif", 10))

        self.create_buttons()

        self.data = Data()
        self.create_data_input()
        self.dl = [self.bitlabel, self.byteslabel, self.KBfield, self.KBlabel,
                    self.bitfield, self.bytesfield, self.MBfield, self.MBlabel,
                    self.GBfield, self.GBlabel, self.TBfield, self.TBlabel,
                    self.PBfield, self.PBlabel, self.KiBfield, self.KiBlabel,
                    self.MiBfield, self.MiBlabel, self.GiBfield, self.GiBlabel,
                    self.TiBfield, self.TiBlabel, self.PiBfield, self.PiBlabel]

        # Main Window
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle("UnitConverter")
        self.setWindowIcon(QtGui.QIcon("data/calculator.png"))

        self.show()

    def create_buttons(self):
        dbtn = QtGui.QPushButton("Data", self)
        dbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        dbtn.resize(dbtn.sizeHint())

        lbtn = QtGui.QPushButton("Length", self)
        lbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        lbtn.resize(lbtn.sizeHint())
        lbtn.move(100, 0)

        vbtn = QtGui.QPushButton("Volume", self)
        vbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        vbtn.resize(vbtn.sizeHint())
        vbtn.move(200, 0)

    def clear_data_input(self):
        for i in self.dl:
            i.deleteLater()

    def create_data_input(self):
        # Input field
        self.bitlabel = QtGui.QLabel(self)
        self.bitfield = QtGui.QLineEdit(self)
        self.bitfield.move(0, 60)
        self.bitlabel.move(130, 60)
        self.bitlabel.setText("bits")
        self.bitfield.textChanged[str].connect(self.data_changed)

        self.byteslabel = QtGui.QLabel(self)
        self.bytesfield = QtGui.QLineEdit(self)
        self.bytesfield.move(180, 60)
        self.byteslabel.move(310, 60)
        self.byteslabel.setText("bytes")
        self.bytesfield.textChanged[str].connect(self.data_changed)

        self.KBlabel = QtGui.QLabel(self)
        self.KBfield = QtGui.QLineEdit(self)
        self.KBfield.move(0, 90)
        self.KBlabel.move(130, 90)
        self.KBlabel.setText("KB")
        self.KBfield.textChanged[str].connect(self.data_changed)

        self.MBlabel = QtGui.QLabel(self)
        self.MBfield = QtGui.QLineEdit(self)
        self.MBfield.move(0, 120)
        self.MBlabel.move(130, 120)
        self.MBlabel.setText("MB")
        self.MBfield.textChanged[str].connect(self.data_changed)

        self.GBlabel = QtGui.QLabel(self)
        self.GBfield = QtGui.QLineEdit(self)
        self.GBfield.move(0, 150)
        self.GBlabel.move(130, 150)
        self.GBlabel.setText("GB")
        self.GBfield.textChanged[str].connect(self.data_changed)

        self.TBlabel = QtGui.QLabel(self)
        self.TBfield = QtGui.QLineEdit(self)
        self.TBfield.move(0, 180)
        self.TBlabel.move(130, 180)
        self.TBlabel.setText("TB")
        self.TBfield.textChanged[str].connect(self.data_changed)

        self.PBlabel = QtGui.QLabel(self)
        self.PBfield = QtGui.QLineEdit(self)
        self.PBfield.move(0, 210)
        self.PBlabel.move(130, 210)
        self.PBlabel.setText("PB")
        self.PBfield.textChanged[str].connect(self.data_changed)

        self.KiBlabel = QtGui.QLabel(self)
        self.KiBfield = QtGui.QLineEdit(self)
        self.KiBfield.move(180, 90)
        self.KiBlabel.move(310, 90)
        self.KiBlabel.setText("KiB")
        self.KiBfield.textChanged[str].connect(self.data_changed)

        self.MiBlabel = QtGui.QLabel(self)
        self.MiBfield = QtGui.QLineEdit(self)
        self.MiBfield.move(180, 120)
        self.MiBlabel.move(310, 120)
        self.MiBlabel.setText("MiB")
        self.MiBfield.textChanged[str].connect(self.data_changed)

        self.GiBlabel = QtGui.QLabel(self)
        self.GiBfield = QtGui.QLineEdit(self)
        self.GiBfield.move(180, 150)
        self.GiBlabel.move(310, 150)
        self.GiBlabel.setText("GiB")
        self.GiBfield.textChanged[str].connect(self.data_changed)

        self.TiBlabel = QtGui.QLabel(self)
        self.TiBfield = QtGui.QLineEdit(self)
        self.TiBfield.move(180, 180)
        self.TiBlabel.move(310, 180)
        self.TiBlabel.setText("TiB")
        self.TiBfield.textChanged[str].connect(self.data_changed)

        self.PiBlabel = QtGui.QLabel(self)
        self.PiBfield = QtGui.QLineEdit(self)
        self.PiBfield.move(180, 210)
        self.PiBlabel.move(310, 210)
        self.PiBlabel.setText("PiB")
        self.PiBfield.textChanged[str].connect(self.data_changed)


    def data_changed(self, text, unit="bits"):

        pass
#         self.data.
#         self.lbl.setText(text)
#         self.lbl.adjustSize()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main():
    app = QtGui.QApplication(sys.argv)

    c = Converter()

    # Delete widget after 10 seconds.
    t = Timer(10, c.deleteLater)
    t.start()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
