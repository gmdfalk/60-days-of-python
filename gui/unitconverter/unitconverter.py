#!/usr/bin/env python2
# TODO: Blank lineedit when entering it.

import decimal
import sys

from PyQt4 import QtGui, QtCore

from conversion import Data


def format_num(num):
    try:
        dec = decimal.Decimal(num)
    except:
        return "bad"
    tup = dec.as_tuple()
    delta = len(tup.digits) + tup.exponent
    digits = ''.join(str(d) for d in tup.digits)
    if delta <= 0:
        zeros = abs(tup.exponent) - len(tup.digits)
        val = '0.' + ('0' * zeros) + digits
    else:
        val = digits[:delta] + ('0' * tup.exponent) + '.' + digits[delta:]
    val = val.rstrip('0')
    if val[-1] == '.':
        val = val[:-1]
    if tup.sign:
        return '-' + val
    return val


class Converter(QtGui.QWidget):

    def __init__(self):

        self.decplaces = 10  # Number of digits after the decimal point.
        self.maxdecplaces = 82  # Maximum number of decimal points.
        self.maxfieldlength = 18  # Maximum length of a QLineEdit field.
        super(Converter, self).__init__()

        # Main Window
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle("UnitConverter")
        self.setWindowIcon(QtGui.QIcon("data/calculator.png"))

        QtGui.QToolTip.setFont(QtGui.QFont("SansSerif", 10))

        tabs = QtGui.QTabWidget()
        datatab = QtGui.QWidget()
        lengthtab = QtGui.QWidget()

        datalayout = QtGui.QVBoxLayout(datatab)
        lengthlayout = QtGui.QVBoxLayout(lengthtab)

        tabs.addTab(datatab, "Data")
        tabs.addTab(lengthtab, "Length")

        button1 = QtGui.QPushButton("button1")
        datalayout.addWidget(button1)

        vbox = QtGui.QVBoxLayout()
#         vbox.addWidget(menu_bar)
        vbox.addWidget(tabs)

        self.setLayout(vbox)

        # Now, show it all.
        self.show()

    def create_byte_layout(self):
        "Create the Data Layout (grid) with LineEdits and Labels"

        data = ["bits", "bytes", "KB", "KiB", "MB", "MiB",
                "GB", "GiB", "TB", "TiB", "PB", "PiB"]
        # Dictionary that holds our QLineEdit fields for later use.
        edits = {unit: QtGui.QLineEdit() for unit in data}

        # Create our positions grid (0,0), (0,1) etc
        pos = [(i, j) for i in range(6) for j in range(4)]

        layout = QtGui.QGridLayout()

        for i in range(len(pos)):
            # Since data is half as long as pos, we use floor division to get
            # the correct corresponding data index from i.
            datapos = data[i // 2]
            # Add a QLabel for uneven positions and QLineEdits for even ones.
            if i % 2:
                layout.addWidget(QtGui.QLabel(datapos), pos[i][0], pos[i][1])
            else:
                layout.addWidget(edits[datapos], pos[i][0], pos[i][1])

        return layout, edits

    def create_buttons_layout(self):

        dbtn = QtGui.QPushButton("Data")
        lbtn = QtGui.QPushButton("Length")
        vbtn = QtGui.QPushButton("Volume")
        nbtn = QtGui.QPushButton("Numbers")
        dbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(dbtn)
        layout.addWidget(lbtn)
        layout.addWidget(vbtn)
        layout.addWidget(nbtn)
        layout.setAlignment(QtCore.Qt.AlignTop)

        return layout

    def create_precision_layout(self):

        prec = QtGui.QLineEdit()
        prec.setText(str(self.decplaces))
        prec.setAlignment(QtCore.Qt.AlignCenter)
        prec.textEdited[str].connect(self.update_precision)


        layout = QtGui.QHBoxLayout()
        layout.addWidget(prec)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        return layout

    def create_data_tab(self, tab):

        self.data = Data()

        data, self.data_edits = self.create_byte_layout()
#         buttons = self.create_buttons_layout()
#         prec = self.create_precision_layout()

        # Patch it all together in a vertical layout.
        data_layout = QtGui.QVBoxLayout(tab)
#         data_layout.addStretch(1)
#         data_layout.addLayout(buttons)
#         data_layout.addLayout(prec)
        data_layout.addLayout(data)


        # Set the text alignment for the LineEdits and connect edits to actions.
        for i in self.data_edits.values():
            i.setAlignment(QtCore.Qt.AlignLeft)
            i.textEdited[str].connect(self.data_changed)
            i.textChanged[str].connect(self.update_data)

    def update_precision(self, text):
        try:
            self.decplaces = int(text)
            self.update_data()
        except ValueError:
            pass  # Fail sil2ently if wrong decplaces format is given.

    def update_data(self):
        for k, v in self.data_edits.items():
            # Exclude the sender from being updated.
            if v != self.sender():
                text = format_num(getattr(self.data, k))
                if "." in text:
                    split = text.split(".")
                    split[1] = split[1][:self.decplaces]
                    text = ".".join(split) if split[1] else split[0]
                v.setText(text)

    def data_changed(self, text):
        for k, v in self.data_edits.items():
            if v == self.sender():
                target = k
                break
        try:
            setattr(self.data, target, float(text))
        except ValueError:
            setattr(self.data, target, 0)


def main():
    "Main entry point."

    app = QtGui.QApplication(sys.argv)
    c = Converter()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
