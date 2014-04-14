"""
    Created on 23 Mar 2014

    @author: Max Demian
"""

import unittest
from address_book import Contacts
from _sqlite3 import OperationalError
import os


class TestContacts(unittest.TestCase):

    def setUp(self):
        self.config = Contacts("test.db")
        self.config.populate_database()

    def tearDown(self):
        self.config.delete_database()

    def test_search(self):
        self.assertEquals(self.config.search("Simpson"), [])
        self.assertNotEquals(self.config.search("Frankfurt"), [])

    def test_insert(self):
        self.config.insert(name="Lisa Simpson", zipcode="80085", city="Springfield",
             street="742 Evergreen Terrace", phone="555 636", mobile="",
             email="chunkylover53@aol.com")
        self.assertNotEquals(self.config.search("Evergreen Terrace"), [])

    def test_show_all(self):
        self.config.show_all()

    def test_delete_table(self):
        self.config.delete_table()
        with self.assertRaises(OperationalError):
            self.config.search("Frankfurt")

    def test_delete_database(self):
        self.config.populate_database()
        self.assertTrue(os.path.isfile("test.db"))
        self.config.delete_database()
        self.assertFalse(os.path.isfile("test.db"))

if __name__ == "__main__":
    unittest.main()
