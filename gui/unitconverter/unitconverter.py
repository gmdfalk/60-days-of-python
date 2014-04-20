#!/usr/bin/env python2
# TODO: Blank lineedit when entering it.
# Use maxline and validator to set input/output constraints for lineedits.
# TODO: roughly complete: mass/weight, length/distance, capacity/volume, temp.
# FIXME: QLayout::addChildLayout: layout "" already has a parent

import decimal
import sys

from PyQt4 import QtGui, QtCore

from conversion import Data, Length, Volume


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


class GUIConverter(QtGui.QWidget):

    def __init__(self):

        self.decplaces = 10  # Number of digits after the decimal point.
        self.maxdecplaces = 82  # Maximum number of decimal points.
        self.maxfieldlength = 18  # Maximum length of a QLineEdit field.
        super(GUIConverter, self).__init__()

        # Main Window
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle("UnitConverter")
        self.setWindowIcon(QtGui.QIcon("data/calculator.png"))

        QtGui.QToolTip.setFont(QtGui.QFont("SansSerif", 10))

        tabs = QtGui.QTabWidget()
        datatab = QtGui.QWidget()
        lengthtab = QtGui.QWidget()
        volumetab = QtGui.QWidget()

        datalayout = self.create_data_tab(datatab)
        lengthlayout = self.create_length_tab(lengthtab)
        volumelayout = self.create_volume_tab(volumetab)

        tabs.addTab(datatab, "Data")
        tabs.addTab(lengthtab, "Length")
        tabs.addTab(volumetab, "Volume")

        mainlayout = QtGui.QVBoxLayout()
        mainlayout.addWidget(tabs)

        self.setLayout(mainlayout)


    def create_grid(self, units, gridsize=4):
        # Dictionary that holds our QLineEdit fields for later use.
        edits = {i[0]: QtGui.QLineEdit() for i in units}

        # Create our positions grid (0,0), (0,1) etc
        pos = [(i, j) for i in range(gridsize) for j in range(4)]

        layout = QtGui.QGridLayout()

        for i in range(len(pos)):
            # Since data is half as long as pos, we use floor division to get
            # the correct corresponding data index from i.
            edit, label = units[i // 2][0], units[i // 2][1]
            # Add a QLabel for uneven positions and QLineEdits for even ones.
            if i % 2:
                layout.addWidget(QtGui.QLabel(label), pos[i][0], pos[i][1])
            else:
                layout.addWidget(edits[edit], pos[i][0], pos[i][1])

        return layout, edits

    def create_decplaces_layout(self):

        prec = QtGui.QLineEdit()
        prec.setFixedWidth(36)
        prec.setAlignment(QtCore.Qt.AlignCenter)
        prec.setText(str(self.decplaces))
        prec.textEdited[str].connect(self.update_decplaces)


        layout = QtGui.QHBoxLayout()
        layout.addWidget(prec)

        return layout

    def create_data_tab(self, tab):

        self.data = Data()

        # List of (unit, label)-pairs to build our grid from.
        units = [("bits", "bits"), ("bytes", "bytes"), ("kilobytes", "kB"),
                ("kibibytes", "KiB"), ("megabytes", "MB"), ("mebibytes", "MiB"),
                ("gigabytes", "GB"), ("gibibytes", "GiB"), ("terrabytes", "TB"),
                ("tebibytes", "TiB"), ("petabytes", "PB"), ("pebibytes", "PiB")]

        grid, self.data_edits = self.create_grid(units, 6)
        prec = self.create_decplaces_layout()

        # Patch it all together in a vertical layout.
        layout = QtGui.QVBoxLayout(tab)
        layout.addLayout(prec)
        layout.addLayout(grid)


        # Set the text alignment for the LineEdits and connect edits to actions.
        for i in self.data_edits.values():
            i.setAlignment(QtCore.Qt.AlignRight)
            i.textEdited[str].connect(self.data_changed)
            i.textChanged[str].connect(self.update_data)
#             i.selectionChanged.connect(i.selectAll)  # FIXME: selectall :(
            # focusInEvent?

        return layout

    def create_length_tab(self, tab):

        self.length = Length()

        units = [("millimeters", "mm"), ("inches", "in"),
                 ("centimeters", "cm"), ("feet", "ft"),
                 ("meters", "m"), ("yards", "yd"),
                 ("kilometers", "km"), ("miles", "mi")]

        grid, self.length_edits = self.create_grid(units)
        prec = self.create_decplaces_layout()

        # Patch it all together in a vertical layout.
        layout = QtGui.QVBoxLayout(tab)
#         data_layout.addStretch(1)
        layout.addLayout(prec)
        layout.addLayout(grid)


        # Set the text alignment for the LineEdits and connect edits to actions.
#         for i in self.data_edits.values():
#             i.setAlignment(QtCore.Qt.AlignRight)
#             i.textEdited[str].connect(self.data_changed)
#             i.textChanged[str].connect(self.update_data)
#             i.selectionChanged.connect(i.selectAll)  # FIXME: selectall :(
            # focusInEvent?

        return layout

    def create_volume_tab(self, tab):

        self.vol = Volume()

        units = [("milliliters", "ml"), ("ounces", "oz"),
                 ("centiliters", "cl"), ("pints", "pt"),
                 ("liters", "l"), ("gallons", "gal"),
                 ("kiloliters", "kl"), ("barrels", "bbl")]

        grid, self.vol_edits = self.create_grid(units)
        prec = self.create_decplaces_layout()

        # Patch it all together in a vertical layout.
        layout = QtGui.QVBoxLayout(tab)
#         data_layout.addStretch(1)
        layout.addLayout(prec)
        layout.addLayout(grid)


        # Set the text alignment for the LineEdits and connect edits to actions.
#         for i in self.data_edits.values():
#             i.setAlignment(QtCore.Qt.AlignRight)
#             i.textEdited[str].connect(self.data_changed)
#             i.textChanged[str].connect(self.update_data)
#             i.selectionChanged.connect(i.selectAll)  # FIXME: selectall :(
            # focusInEvent?

        return layout

    def create_color_button(self):
        col = QtGui.QColor(0, 0, 0)

        self.btn = QtGui.QPushButton('Dialog', self)
        self.btn.move(20, 20)

        self.btn.clicked.connect(self.show_color_picker)

        self.frm = QtGui.QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }"
            % col.name())
        self.frm.setGeometry(130, 22, 100, 100)

    def show_color_picker(self):

        col = QtGui.QColorDialog.getColor()

        if col.isValid():
            self.frm.setStyleSheet("QWidget { background-color: %s }"
                % col.name())

    def update_decplaces(self, text):
        try:
            self.decplaces = int(text)
            self.update_data()
        except ValueError:
            pass  # Fail silently if wrong decplaces format is given.

    def update_data(self):
        "Update the values of all Data/Bytes QLineEdits"
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
        "When a Data/Bytes QLineEdit was changed, we call the conversion logic"
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
    c = GUIConverter()
    c.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
