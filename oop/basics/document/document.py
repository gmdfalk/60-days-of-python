"""
    Created on 26 Mar 2014

    @author: Max Demian
"""

class Document(object):

    def __init__(self):
        self.characters = []
        self.cursor = Cursor(self)
        self.filename = ""

    def insert(self, character):
        if not hasattr(character, "character"):
            character = Character(character)
        self.characters.insert(self.cursor.position, character)
        self.cursor.forward()

    def delete(self):
        print self.characters
        del self.characters[self.cursor.position]

    def save(self, filename):
        self.filename = filename
        with open(self.filename, "w") as f:
            f.write(''.join(self.characters))

    @property
    def string(self):
        return "".join((str(c) for c in self.characters))

    def home(self):
        while self.document.characters[
                self.position - 1].character != "\n":
            self.position -= 1
            if self.position == 0:
                # Got to beginning of file before newline.
                break

    def end(self):
        while self.position < len(self.document.characters) and\
                self.document.characters[self.position].characters != "\n":
            self.position += 1


class Cursor(object):

    def __init__(self, document):
        self.document = document
        self.position = 0

    def forward(self):
        self.position += 1

    def back(self):
        self.position -= 1

    def home(self):
        while self.document.characters[self.position - 1] != "\n":
            self.position -= 1
            if self.position == 0:
                break

    def end(self):
        while self.position < len(self.document.characters
            ) and self.document.characters[self.position] != "\n":
            self.position += 1


# FIXME: Inherit from string to allow .join() method on Characters. Should
# probably solved some other way.
class Character(str):

    def __init__(self, character, bold=False, italic=False, underline=False):
        assert len(character) == 1
        self.character = character
        self.bold = bold
        self.italic = italic
        self.underline = underline

    def __str__(self):
        bold = "*" if self.bold else ""
        italic = "/" if self.italic else ""
        underline = "_" if self.underline else ""
        return bold + italic + underline + self.character

if __name__ == "__main__":
    d = Document()
    string = ["h", "e", "l", "l", "o", "\n", "w", "o", "r", "l", "d", "!"]
    for i in string:
        d.insert(i)
    d.insert(Character('w', bold=True))
    d.insert(Character('o', italic=True))
    d.insert(Character('r', underline=True))
    d.insert(Character('1', bold=True))
    d.cursor.home()
    d.delete()
    d.insert('W')
    print d.string
    d.characters[0].underline = True
    print d.string
