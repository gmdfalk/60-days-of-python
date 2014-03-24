"""
    Created on 22 Mar 2014
    @author: Max Demian
"""

import sys
from notebook import Notebook


class Menu(object):
    "Display a menu and respond to choices when run"
    def __init__(self):
        self.notebook = Notebook()
        self.choices = {
                        "1": self.show_notes,
                        "2": self.search_notes,
                        "3": self.add_note,
                        "4": self.modify_note,
                        "5": self.quit
                        }

    def display_menu(self):
        print "1: show notes, 2: search, 3: add, 4: modify, 5: quit"

    def run(self):
        "Display the menu and respond to choices"
        while True:
            self.display_menu()
            choice = raw_input("> ")
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print "{0} is not a valid choice".format(choice)

    def show_notes(self, notes=None):
        if not notes:
            notes = self.notebook.notes
        for note in notes:
            print "{0}, {1}:\n{2}".format(
                note.id, note.tags, note.memo)

    def search_notes(self):
        pattern = raw_input("Search for: ")
        notes = self.notebook.search(pattern)
        self.show_notes(notes)

    def add_note(self):
        memo = raw_input("Enter a memo: ")
        self.notebook.new_note(memo)
        print "Your note has been added."

    def modify_note(self):
        note_id = int(raw_input("Enter a note id: "))
        if not self.notebook._find_note(note_id):
            return
        memo = raw_input("Enter a memo: ")
        tags = raw_input("Enter tags: ")
        if memo:
            self.notebook.modify_memo(note_id, memo)
        if tags:
            self.notebook.modify_tags(note_id, tags)

    def quit(self):
        print "Thanks for using your notebook today."
        sys.exit()

if __name__ == "__main__":
    Menu().run()
