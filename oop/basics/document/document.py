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
        return "".join(self.characters)


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

if __name__ == "__main__":
    d = Document()
    string = ["h", "e", "l", "l", "o", "\n", "w", "o", "r", "l", "d", "!"]
    for i in string:
        d.insert(i)
    print d.string
