"""
    Created on 23 Mar 2014

    @author: Max Demian
"""

import unittest
from address_book import Contacts
from _sqlite3 import OperationalError
import os


class Test(unittest.TestCase):

    def setUp(self):
        self.c = Contacts("test.db")
        self.c.populate_database()

    def tearDown(self):
        self.c.delete_database()

    def test_search(self):
        self.assertEquals(self.c.search("Simpson"), [])
        self.assertNotEquals(self.c.search("Frankfurt"), [])

    def test_insert(self):
        self.c.insert(name="Lisa Simpson", zipcode="80085", city="Springfield",
             street="742 Evergreen Terrace", phone="555 636", mobile="",
             email="chunkylover53@aol.com")
        self.assertNotEquals(self.c.search("Evergreen Terrace"), [])

    def test_show_all(self):
        self.c.show_all()

    def test_delete_table(self):
        self.c.delete_table()
        with self.assertRaises(OperationalError):
            self.c.search("Frankfurt")

    def test_delete_database(self):
        self.c.populate_database()
        self.assertTrue(os.path.isfile("test.db"))
        self.c.delete_database()
        self.assertFalse(os.path.isfile("test.db"))

if __name__ == "__main__":
    unittest.main()
