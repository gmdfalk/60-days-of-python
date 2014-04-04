"""
    Created on 26 Mar 2014

    @author: Max Demian
"""

import unittest
from os import remove
from document import Document


class TestDocument(unittest.TestCase):

    def setUp(self):
        self.d = Document()
        self.d.insert("a")

    def test_cursor(self):
        self.assertEqual(self.d.cursor.position, 1)
        self.d.save("tst")
        try:
            remove("tst")
        except OSError:
            pass
        self.d.cursor.back()
        self.d.delete()
        self.assertEqual(self.d.cursor.position, 0)

    def test_multiple_chars_and_escape(self):
        self.d.cursor.home()
        self.d.delete()
        string = ["h", "e", "l", "l", "o", "\n", "w", "o", "r", "l", "d", "!"]
        for i in string:
            self.d.insert(i)
        self.assertEqual(self.d.string, "hello\nworld!")

    def test_string_property(self):
        self.assertEqual(self.d.string, "a")

if __name__ == "__main__":
    unittest.main()
