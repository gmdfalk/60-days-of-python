#!/usr/bin/env python2
# TODO: Blank lineedit when entering it or select all text.
# Use maxline and validator to set input/output constraints for lineedits.
# TODO: roughly complete: mass/weight, length/distance, capacity/volume, temp.

import sys

from PyQt4 import QtGui, QtCore

from conversion import Data, Length, Volume


class GUIConverter(QtGui.QWidget):

    def __init__(self):

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
        weighttab = QtGui.QWidget()
        numberstab = QtGui.QWidget()
        colorstab = QtGui.QWidget()

        self.create_data_tab(datatab)
        self.create_length_tab(lengthtab)
        self.create_volume_tab(volumetab)

        tabs.addTab(datatab, "Data")
        tabs.addTab(lengthtab, "Length")
        tabs.addTab(volumetab, "Volume")
        tabs.addTab(weighttab, "Weight")
        tabs.addTab(numberstab, "Nums")
        tabs.addTab(colorstab, "Colors")

        mainlayout = QtGui.QVBoxLayout()
        mainlayout.addWidget(tabs)

        self.setLayout(mainlayout)


    def create_grid(self, units, gridsize=4):
        "Creates the grid of conversion unit QLineEdits and QLabels for a tab."
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

    def create_data_tab(self, tab):

        self.data = Data()

        # List of (unit, label)-pairs to build our grid from.
        units = [("bits", "bits"), ("bytes", "bytes"), ("kilobytes", "kB"),
                ("kibibytes", "KiB"), ("megabytes", "MB"), ("mebibytes", "MiB"),
                ("gigabytes", "GB"), ("gibibytes", "GiB"), ("terrabytes", "TB"),
                ("tebibytes", "TiB"), ("petabytes", "PB"), ("pebibytes", "PiB")]

        grid, self.data_edits = self.create_grid(units, 6)
        prec = self.create_precision_layout("data")

        # Patch it all together in a vertical layout.
        layout = QtGui.QVBoxLayout(tab)
        layout.addLayout(prec)
        layout.addLayout(grid)

        # Set the text alignment for the LineEdits and connect edits to actions.
        for i in self.data_edits.values():
            i.setAlignment(QtCore.Qt.AlignRight)
            i.textEdited[str].connect(self.data_text_changed)
            i.textChanged[str].connect(self.update_data_edits)
#             i.selectionChanged.connect(i.selectAll)  # FIXME: selectall :(
            # focusInEvent?

    def create_length_tab(self, tab):

        self.length = Length()

        units = [("millimeters", "mm"), ("inches", "in"),
                 ("centimeters", "cm"), ("feet", "ft"),
                 ("meters", "m"), ("yards", "yd"),
                 ("kilometers", "km"), ("miles", "mi")]

        grid, self.length_edits = self.create_grid(units)
        prec = self.create_precision_layout("length")

        layout = QtGui.QVBoxLayout(tab)
        layout.addLayout(prec)
        layout.addLayout(grid)

        for i in self.length_edits.values():
            i.setAlignment(QtCore.Qt.AlignRight)
            i.textEdited[str].connect(self.length_text_changed)
            i.textChanged[str].connect(self.update_length_edits)

    def create_volume_tab(self, tab):

        self.volume = Volume()

        units = [("milliliters", "ml"), ("ounces", "oz"),
                 ("centiliters", "cl"), ("pints", "pt"),
                 ("liters", "l"), ("gallons", "gal"),
                 ("kiloliters", "kl"), ("barrels", "bbl")]

        grid, self.volume_edits = self.create_grid(units)
        prec = self.create_precision_layout("volume")

        # Patch it all together in a vertical layout.
        layout = QtGui.QVBoxLayout(tab)
        layout.addLayout(prec)
        layout.addLayout(grid)

        for i in self.volume_edits.values():
            i.setAlignment(QtCore.Qt.AlignRight)
            i.textEdited[str].connect(self.volume_text_changed)
            i.textChanged[str].connect(self.update_volume_edits)

    def create_precision_layout(self, unittype):
        "QLineEdit that allows adjusting of decimal places."
        prec = QtGui.QLineEdit()
        prec.setFixedWidth(36)
        prec.setAlignment(QtCore.Qt.AlignCenter)
        if unittype == "data":
            prec.setText(str(self.data.precision))
            prec.textEdited[str].connect(self.update_data_precision)
        if unittype == "length":
            prec.setText(str(self.length.precision))
            prec.textEdited[str].connect(self.update_length_precision)
        if unittype == "volume":
            prec.setText(str(self.volume.precision))
            prec.textEdited[str].connect(self.update_volume_precision)
        if unittype == "weight":
            prec.setText(str(self.weight.precision))
            prec.textEdited[str].connect(self.update_weight_precision)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(prec)

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

    def update_data_precision(self, text):
#         try:
        print "setting data precision to", text
        self.data.precision = int(text)
        self.update_data_edits()
#         except ValueError:
#             pass

    def update_length_precision(self, text):
        try:
            self.length.precision = int(text)
            self.update_length_edits()
        except ValueError:
            pass

    def update_volume_precision(self, text):
        try:
            self.volume.precision = int(text)
            self.update_volume_edits()
        except ValueError:
            pass

#     def update_weight_precision(self, text):
#         try:
#             self.weight.precision = int(text)
#             self.update_weight_edits()
#         except ValueError:
#             pass

    def update_edits(self, unittype, edit):
        for k, v in edit.items():
            # Exclude the sender from being updated.
            if v != self.sender():
                text = getattr(unittype, k)
                v.setText(text)

    def text_changed(self, text, unittype, edits):
        "Set the correct unit in conversion.py to the text we just received."
        for k, v in edits.items():
            if v == self.sender():
                unit = k
                break
        try:
            setattr(unittype, unit, float(text))
        except ValueError:
            setattr(unittype, unit, 0)

    def update_data_edits(self):
        "Update the values of all Data/Bytes QLineEdits"
        unittype, edit = self.data, self.data_edits
        self.update_edits(unittype, edit)

    def update_length_edits(self):
        "Update the values of all Length QLineEdits"
        unittype, edit = self.length, self.length_edits
        self.update_edits(unittype, edit)

    def update_volume_edits(self):
        "Update the values of all Volume QLineEdits"
        unittype, edit = self.volume, self.volume_edits
        self.update_edits(unittype, edit)

    def data_text_changed(self, text):
        "When a Data/Bytes QLineEdit was changed, we pass its text along"
        unittype, edits = self.data, self.data_edits
        self.text_changed(text, unittype, edits)

    def length_text_changed(self, text):
        "When a Length QLineEdit was changed, we pass its text along"
        unittype, edits = self.length, self.length_edits
        self.text_changed(text, unittype, edits)

    def volume_text_changed(self, text):
        "When a Volume QLineEdit was changed, we pass its text along"
        unittype, edits = self.volume, self.volume_edits
        self.text_changed(text, unittype, edits)


def main():
    "Main entry point."

    app = QtGui.QApplication(sys.argv)
    c = GUIConverter()
    c.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
