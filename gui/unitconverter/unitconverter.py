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

    def __init__(self, app):

        self.precision = 10  # Maximum number of decimal points.
        self.maxlength = 18  # Defunct. Max length of a QLineEdit field.
        self.app = app
        super(Converter, self).__init__()
        self.initUI()

    def initUI(self):

        QtGui.QToolTip.setFont(QtGui.QFont("SansSerif", 10))

        # Main Window
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle("UnitConverter")
        self.setWindowIcon(QtGui.QIcon("data/calculator.png"))

        # Create the initial UI elements.
        self.create_data_ui()

        # Now, show it all.
        self.show()

    def clear_gui(self):
        "Delete elements so we can switch to a different UI mode."

        for widget in self.app.allWidgets():
            if isinstance(widget, QtGui.QLineEdit):
                widget.deleteLater()
            if isinstance(widget, QtGui.QLabel):
                widget.deleteLater()

    def create_data_layout(self):
        "Create the Data Layout (grid) with LineEdits and Labels"

        data = ["bits", "bytes", "KB", "KiB", "MB", "MiB",
                "GB", "GiB", "TB", "TiB", "PB", "PiB"]
        # Dictionary that holds our QLineEdit fields for later use.
        edits = {unit: QtGui.QLineEdit() for unit in data}

        pos = [(0, 0), (0, 1), (0, 2), (0, 3),
               (1, 0), (1, 1), (1, 2), (1, 3),
               (2, 0), (2, 1), (2, 2), (2, 3),
               (3, 0), (3, 1), (3, 2), (3, 3),
               (4, 0), (4, 1), (4, 2), (4, 3),
               (5, 0), (5, 1), (5, 2), (5, 3)]
        # GRID
        layout = QtGui.QGridLayout()

        for i in range(len(pos)):
            # Since data is half as long as pos, we use floor division to get
            # the correct corresponding data index from i.
            datapos = data[i // 2]
            # Add a QLabel for uneven positions and QLineEdits for even ones.
            if i % 2:
                layout.addWidget(QtGui.QLabel(datapos), pos[i][0], pos[i][1])
            else:
                field = edits[datapos]
                # Align text on the right.
                layout.addWidget(field, pos[i][0], pos[i][1])

        return layout, edits

    def create_buttons_layout(self):

        dbtn = QtGui.QPushButton("Data")
        lbtn = QtGui.QPushButton("Length")
        vbtn = QtGui.QPushButton("Volume")
        nbtn = QtGui.QPushButton("Numbers")
        dbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)

        layout = QtGui.QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(dbtn)
        layout.addWidget(lbtn)
        layout.addWidget(vbtn)
        layout.addWidget(nbtn)

        return layout

    def create_precision_layout(self):

        prec = QtGui.QLineEdit()
        prec.setText(str(self.precision))
        prec.setAlignment(QtCore.Qt.AlignCenter)
        prec.textEdited[str].connect(self.update_precision)


        layout = QtGui.QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(prec)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        return layout

    def create_data_ui(self):

        self.data = Data()

        data, self.edits = self.create_data_layout()
        buttons = self.create_buttons_layout()
        prec = self.create_precision_layout()

        # Patch it all together in a vertical layout.
        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(buttons)
        vbox.addLayout(prec)
        vbox.addLayout(data)

        self.setLayout(vbox)

        # Set the text alignment for the LineEdits and connect edits to actions.
        for i in self.edits.values():
            i.setAlignment(QtCore.Qt.AlignLeft)
            i.textEdited[str].connect(self.data_changed)
            i.textChanged[str].connect(self.update_data)

    def update_precision(self, text):
        try:
            self.precision = int(text)
            self.update_data()
        except ValueError:
            pass  # Fail sil2ently if wrong precision format is given.

    def update_data(self):
        for k, v in self.edits.items():
            # Exclude the sender from being updated.
            if v != self.sender():
                text = format_num(getattr(self.data, k))
                if "." in text:
                    split = text.split(".")
                    split[1] = split[1][:self.precision]
                    text = ".".join(split) if split[1] else split[0]
                v.setText(text)

    def data_changed(self, text):
        for k, v in self.edits.items():
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
    c = Converter(app)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
