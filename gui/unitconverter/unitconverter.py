#!/usr/bin/env python2
# FIXME: Leading 0 for Base.
import sys

from PyQt4 import QtGui, QtCore

from conversion import Base, Data, Length, Volume, Weight, rot


class SelectAllLineEdit(QtGui.QLineEdit):
    "Overloaded QLineEdit to select all text when clicked into."

    def mousePressEvent (self, e):
        self.selectAll()

class SelectAllTextEdit(QtGui.QTextEdit):
    "Overloaded QLineEdit to select all text when clicked into."

    def mousePressEvent (self, e):
        self.selectAll()

class GUIConverter(QtGui.QWidget):

    def __init__(self):

        super(GUIConverter, self).__init__()

        # Main Window
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle("UnitConverter")
        self.setWindowIcon(QtGui.QIcon("icon.png"))

        QtGui.QToolTip.setFont(QtGui.QFont("SansSerif", 10))

        tabs = QtGui.QTabWidget()
        basetab = QtGui.QWidget()
        caesartab = QtGui.QWidget()
        datatab = QtGui.QWidget()
        lengthtab = QtGui.QWidget()
        volumetab = QtGui.QWidget()
        weighttab = QtGui.QWidget()

        self.create_base_tab(basetab)
        self.create_caesar_tab(caesartab)
        self.create_data_tab(datatab)
        self.create_length_tab(lengthtab)
        self.create_volume_tab(volumetab)
        self.create_weight_tab(weighttab)

        tabs.addTab(basetab, "Base")
        tabs.addTab(datatab, "Data")
        tabs.addTab(lengthtab, "Length")
        tabs.addTab(volumetab, "Volume")
        tabs.addTab(weighttab, "Weight")
        tabs.addTab(caesartab, "Caesar")

        mainlayout = QtGui.QVBoxLayout()
        mainlayout.addWidget(tabs)

        self.setLayout(mainlayout)

    def create_grid(self, units, gridsize=4):
        "Creates the grid of conversion unit QLineEdits and QLabels for a tab."
        # Dictionary that holds our QLineEdit fields for later use.
        edits = {i[0]: SelectAllLineEdit() for i in units}

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

    def create_base_tab(self, tab):

        self.base = Base()

        # List of (unit, label)-pairs to build our grid from.
        bases = (2, 3, 5, 8, 10, 12, 16, 20, 32, 36, 60, 64)
        units = [(i, str(i)) for i in bases]

        grid, self.base_edits = self.create_grid(units, 6)
        colors = self.create_color_layout()

        # Patch it all together in a vertical layout.
        layout = QtGui.QVBoxLayout(tab)
        layout.addLayout(colors)
        layout.addLayout(grid)

        # Set the text alignment for the LineEdits and connect edits to actions.
        for i in self.base_edits.values():
            i.setAlignment(QtCore.Qt.AlignRight)
            i.textEdited[str].connect(self.base_text_changed)
            i.textEdited[str].connect(self.update_base_edits)

    def create_caesar_tab(self, tab):
        "Tab that does encoding/decoding of caesar ciphers."
        # Default to rot13.
        self.caesar_shift = 13
        self.caesar_edits = {"input": QtGui.QTextEdit(),
                             "output": SelectAllTextEdit()}

        # Put those QLineEdits into a vertical splitter.
        splitter = QtGui.QSplitter(QtCore.Qt.Vertical, self)
        splitter.addWidget(self.caesar_edits["input"])
        splitter.addWidget(self.caesar_edits["output"])

        grid = QtGui.QGridLayout()
#         grid.setSpacing(10)
        grid.addWidget(splitter)

        shift = self.create_caesarshift_layout()

        # Patch it all together in a vertical layout.
        layout = QtGui.QVBoxLayout(tab)
        layout.addLayout(shift)
        layout.addLayout(grid)

        # Set the text alignment for the LineEdits and connect edits to actions.
        self.caesar_edits["input"].textChanged.connect(self.update_caesar_edits)
        self.caesar_edits["output"].setReadOnly(True)
        # TODO: Make the lineedits interchangable (input/output).

    def create_data_tab(self, tab):

        self.data = Data()

        # List of (unit, label)-pairs to build our grid from.
        units = [("bits", "bits"), ("bytes", "bytes"), ("kilobytes", "kB"),
                ("kibibytes", "KiB"), ("megabytes", "MB"), ("mebibytes", "MiB"),
                ("gigabytes", "GB"), ("gibibytes", "GiB"), ("terrabytes", "TB"),
                ("tebibytes", "TiB"), ("petabytes", "PB"), ("pebibytes", "PiB")]

        grid, self.data_edits = self.create_grid(units, 6)
        prec = self.create_decplaces_layout("data")

        # Patch it all together in a vertical layout.
        layout = QtGui.QVBoxLayout(tab)
        layout.addLayout(prec)
        layout.addLayout(grid)

        # Set the text alignment for the LineEdits and connect edits to actions.
        for i in self.data_edits.values():
            i.setAlignment(QtCore.Qt.AlignRight)
            i.textEdited[str].connect(self.data_text_changed)
            i.textEdited.connect(self.update_data_edits)
#             i.selectionChanged.connect(i.selectAll)  # FIXME: selectall :(
            # focusInEvent?

    def create_length_tab(self, tab):

        self.length = Length()

        units = [("millimeters", "mm"), ("inches", "in"),
                 ("centimeters", "cm"), ("feet", "ft"),
                 ("meters", "m"), ("yards", "yd"),
                 ("kilometers", "km"), ("miles", "mi")]

        grid, self.length_edits = self.create_grid(units)
        prec = self.create_decplaces_layout("length")

        layout = QtGui.QVBoxLayout(tab)
        layout.addLayout(prec)
        layout.addLayout(grid)

        for i in self.length_edits.values():
            i.setAlignment(QtCore.Qt.AlignRight)
            i.textEdited[str].connect(self.length_text_changed)
            i.textEdited[str].connect(self.update_length_edits)

    def create_volume_tab(self, tab):

        self.volume = Volume()

        units = [("milliliters", "ml"), ("ounces", "oz"),
                 ("centiliters", "cl"), ("pints", "pt"),
                 ("liters", "l"), ("gallons", "gal"),
                 ("kiloliters", "kl"), ("barrels", "bbl")]

        grid, self.volume_edits = self.create_grid(units)
        prec = self.create_decplaces_layout("volume")

        # Patch it all together in a vertical layout.
        layout = QtGui.QVBoxLayout(tab)
        layout.addLayout(prec)
        layout.addLayout(grid)

        for i in self.volume_edits.values():
            i.setAlignment(QtCore.Qt.AlignRight)
            i.textEdited[str].connect(self.volume_text_changed)
            i.textEdited[str].connect(self.update_volume_edits)

    def create_weight_tab(self, tab):

        self.weight = Weight()

        units = [("milligrams", "mg"), ("drams", "dr"),
                 ("grams", "g"), ("ounces", "oz"),
                 ("kilograms", "kg"), ("pounds", "lbs"),
                 ("tons", "t"), ("ustons", "t (US)")]

        grid, self.weight_edits = self.create_grid(units)
        prec = self.create_decplaces_layout("weight")

        # Patch it all together in a vertical layout.
        layout = QtGui.QVBoxLayout(tab)
        layout.addLayout(prec)
        layout.addLayout(grid)

        for i in self.weight_edits.values():
            i.setAlignment(QtCore.Qt.AlignRight)
            i.textEdited[str].connect(self.weight_text_changed)
            i.textEdited[str].connect(self.update_weight_edits)

    def create_caesarshift_layout(self):
        "QLineEdit that allows adjusting of decimal places."
        shift = SelectAllLineEdit()
        shift.setFixedWidth(36)
        shift.setAlignment(QtCore.Qt.AlignCenter)
        shift.setText(str(self.caesar_shift))
        shift.textEdited[str].connect(self.update_caesar_shift)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(shift)

        return layout

    def create_decplaces_layout(self, unittype):
        "QLineEdit that allows adjusting of decimal places."
        prec = SelectAllLineEdit()
        prec.setFixedWidth(36)
        prec.setAlignment(QtCore.Qt.AlignCenter)
        if unittype == "data":
            prec.setText(str(self.data.decplaces))
            prec.textEdited[str].connect(self.update_data_decplaces)
        if unittype == "length":
            prec.setText(str(self.length.decplaces))
            prec.textEdited[str].connect(self.update_length_decplaces)
        if unittype == "volume":
            prec.setText(str(self.volume.decplaces))
            prec.textEdited[str].connect(self.update_volume_decplaces)
        if unittype == "weight":
            prec.setText(str(self.weight.decplaces))
            prec.textEdited[str].connect(self.update_weight_decplaces)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(prec)

        return layout

    def create_color_layout(self):

        button = QtGui.QPushButton("ColorPicker", self)
        button.clicked.connect(self.show_color_picker)

        self.frm = QtGui.QFrame(self)
        self.frm.setGeometry(130, 22, 100, 100)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(button)

        return layout

    def show_color_picker(self):

        col = QtGui.QColorDialog.getColor()
#
        # Prints the selected color as hex value to console.
        if col.isValid():
            print col.name()

    def update_caesar_shift(self, text):
        try:
            self.caesar_shift = int(text)
            self.update_caesar_edits()
        except ValueError:
            pass

    def update_data_decplaces(self, text):
        try:
            self.data.decplaces = int(text)
            self.update_data_edits()
        except ValueError:
            pass

    def update_length_decplaces(self, text):
        try:
            self.length.decplaces = int(text)
            self.update_length_edits()
        except ValueError:
            pass

    def update_volume_decplaces(self, text):
        try:
            self.volume.decplaces = int(text)
            self.update_volume_edits()
        except ValueError:
            pass

    def update_weight_decplaces(self, text):
        try:
            self.weight.decplaces = int(text)
            self.update_weight_edits()
        except ValueError:
            pass

    def update_edits(self, unittype, edit):
        "Update all QLineEdits of the unittype (e.g. data)."
        for k, v in edit.items():
            # Exclude the sender from being updated.
            if v != self.sender():
                text = getattr(unittype, k)
                v.setText(text)

    def update_base_edits(self):
        "Update the values of all Base/Numbers QLineEdits"
        for k, v in self.base_edits.items():
            # Exclude the sender from being updated.
            if v != self.sender():
                dec = getattr(self.base, "_decimal")
                text = self.base.from_decimal(dec, k)
                v.setText(text)

    def update_caesar_edits(self):
        "Set the correct unit in conversion.py to the text we just received."
        text = self.caesar_edits["input"].toPlainText()

        output = self.caesar_edits["output"]
        message = rot(str(text), self.caesar_shift)
        output.setText(message)

    def update_data_edits(self):
        self.update_edits(self.data, self.data_edits)

    def update_length_edits(self):
        self.update_edits(self.length, self.length_edits)

    def update_volume_edits(self):
        self.update_edits(self.volume, self.volume_edits)

    def update_weight_edits(self):
        self.update_edits(self.weight, self.weight_edits)

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

    def base_text_changed(self, text):
        "When a Base/Numbers QLineEdit was changed, we pass its text along"
        for k, v in self.base_edits.items():
            if v == self.sender():
                base = k
                break

        dec = self.base.to_decimal(text, base)
        setattr(self.base, "_decimal", dec)

    def data_text_changed(self, text):
        self.text_changed(text, self.data, self.data_edits)

    def length_text_changed(self, text):
        self.text_changed(text, self.length, self.length_edits)

    def volume_text_changed(self, text):
        self.text_changed(text, self.volume, self.volume_edits)

    def weight_text_changed(self, text):
        self.text_changed(text, self.weight, self.weight_edits)


def main():
    "Main entry point."

    app = QtGui.QApplication(sys.argv)
    c = GUIConverter()
    c.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
