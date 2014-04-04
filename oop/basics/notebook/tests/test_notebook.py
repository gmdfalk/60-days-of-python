"""
    Created on 22 Mar 2014
    @author: Max Demian
"""

import datetime
import unittest

from ..notebook import Note, Notebook


class TestNote(unittest.TestCase):

    def test_note(self):
        note = Note()
        self.assertEqual(note.creation_date, datetime.date.today())

    def test_memo(self):
        note = Note("this is a test")
        self.assertEqual(note.memo, "this is a test")

    def test_match(self):
        note = Note("pen")
        self.assertEqual(note.match("pen"), True)

class TestNotebook(unittest.TestCase):
    def setUp(self):
        self.book = Notebook()
        self.note = Note("hey", "test")
        self.book.new_note(self.note, "test_1")
        self.book.new_note(self.note, "test_2")

    def test_modify(self):
#         self.assertEqual(self.book.notes[0].memo, "test 1")
#         self.book.modify_memo(1, "hi world")
#         self.assertEqual(self.book.notes[0].memo, "hi world")
        pass

    def test_len(self):
        self.assertEqual(len(self.book.notes), 2)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_note']
    unittest.main()
