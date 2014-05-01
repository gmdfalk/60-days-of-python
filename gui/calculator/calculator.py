#!/usr/bin/env python2
# TODO: Fix stylesheets for lineedits.
# setMinimumSize (something is setting this. unset it)
# Store buttons in variables.

import sys

from PyQt4 import QtGui, QtCore

from calculation import evaluate


class SelectAllLineEdit(QtGui.QLineEdit):
    "Overloaded QLineEdit to select all text when clicked into."

    def mousePressEvent (self, e):
        self.selectAll()


class GUICalculator(QtGui.QWidget):

    def __init__(self):
        super(GUICalculator, self).__init__()
        self.setGeometry(500, 300, 350, 300)
        self.setWindowTitle("Calculator")
        self.setWindowIcon(QtGui.QIcon("calculator.png"))

        edits = self.create_edit_layout()
        grid = self.create_button_layout()

        mainlayout = QtGui.QVBoxLayout()
        mainlayout.addLayout(edits)
        mainlayout.addLayout(grid)

        self.setLayout(mainlayout)

    def create_button_layout(self):
        "Creates the grid of calculator buttons."

        labels = ["Close", "mrc", "m+", "m-",
                  "Clear", "(", ")", "!",
                  "sqrt", "pow", "%", "/",
                  "7", "8", "9", "*",
                  "4", "5", "6", "-",
                  "1", "2", "3", "+",
                  "0", ".", "C", "="]

        buttons = {i: QtGui.QPushButton(i) for i in labels}

        for l in labels:
            btn = buttons[l]
            if l in "0123456789.-+/%()**":
                func = lambda: self.in_edit.setText(self.in_edit.text() + l)
                btn.clicked.connect(func)
            elif l == "=":
                btn.clicked.connect(self.equals_pressed)
            elif l == "Close":
                btn.clicked.connect(self.close_pressed)
            elif l == "Clear":
                btn.clicked.connect(self.clear_pressed)
            elif l == "sqrt":
                btn.clicked.connect(self.sqrt_pressed)
            elif l == "pow":
                btn.clicked.connect(self.pow_pressed)

        # Create our positions grid (0,0), (0,1) etc.
        pos = [(i, j) for i in range(7) for j in range(4)]

        layout = QtGui.QGridLayout()

        for i in range(len(labels)):
            layout.addWidget(buttons[labels[i]], pos[i][0], pos[i][1])

        return layout

    def create_edit_layout(self):
        self.in_edit = QtGui.QLineEdit()
        self.in_edit.setStyleSheet("padding: 0px;")
        self.in_edit.returnPressed.connect(self.update_output)
        self.out_edit = SelectAllLineEdit()
        self.out_edit.setStyleSheet("padding: 0px;")
        self.out_edit.setReadOnly(True)
        layout = QtGui.QVBoxLayout()
        layout.setSpacing(0)
        layout.addWidget(self.in_edit)
        layout.addWidget(self.out_edit)

        return layout

    def close_pressed(self):
        print "close pressed"

    def c_pressed(self):
        print "c pressed"

    def clear_pressed(self):
        print "clear pressed"

    def sqrt_pressed(self):
        print "sqrt pressed"

    def pow_pressed(self):
        print "pow pressed"

    def equals_pressed(self):
        print "equals pressed"

    def update_output(self):
        output = evaluate(str(self.in_edit.text()))
        if output:
            self.out_edit.setText(str(output))
            self.in_edit.setText("")

def main():
    app = QtGui.QApplication(sys.argv)
    c = GUICalculator()
    c.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
