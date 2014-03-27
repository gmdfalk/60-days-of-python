# coding: utf-8

import sqlite3 as sql
import os

class Contacts(object):
    "Manages your contacts in a sqlite3 database"

    def __init__(self, db_file="addresses.db", table="Addresses"):
        self.table = table
        # Create and/or connect to our database.
        self.db_file = db_file
        self.db = sql.connect(self.db_file)
        # Fix encoding issues.
        self.db.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
        # And create the cursor so we can perform database actions.
        self.cur = self.db.cursor()

    def populate_database(self):
        "Creates a sample database to work with"
        addresses = (
            ("Max Demian", "60329", "Frankfurt", "Gutleutstraße 214",
             "069 741 382", "0176 241 332", "mikar@gmx.net"),
            ("Mathias Hoover", "54340", "Schleich", "Güntzelstr. 12",
             "06507 58 02 52", "317 461 1232", "hoovercraft@lol.cat"),
            ("Dirk Vogt", "92303", "Neumarkt", "Luebecker Tordamm 1",
             "09181 75 77 80", "7024380985", "DirkVogt@armyspy.com"),
            ("Barbara Baier", "15230", "Frankfurt (Oder)", "Kirchstr. 36",
             "05704 27 12 54", "1-323-472-0089", "bbaier@jourrapi.de")
        )

        with self.db:
            self.cur.execute("DROP TABLE IF EXISTS {}".format(self.table))
            self.cur.execute("CREATE TABLE {}(Name TEXT, ZIP Text, City Text,\
                              Street Text, Phone Text, Mobile Text,\
                              Email TEXT)".format(self.table))
            self.cur.executemany("INSERT INTO {} VALUES(?, ?, ?, ?, ?, ?, ?\
                                 )".format(self.table), addresses)

    def insert(self, name="", zip="", city="", street="",
               phone="", mobile="", email=""):
        with self.db:
            self.cur.execute("INSERT INTO {} VALUES({}, {}, {}, {}, {},\
                              {}, {})".format(self.table, name, zip, city,
                                             street, phone, mobile, email))

    def search(self):
        pass

    def show(self):
        # FIXME: SQLite wants to use ASCII here so we abide, for now.
        with self.db:
            self.db.text_factory = str
            self.cur.execute("SELECT * from {}".format(self.table))
            for i in self.cur.fetchall():
                print "{}, {} {}, {}".format(i[0], i[1], i[2], i[3])
                print "{}, {}, mobile: {}\n".format(i[6], i[4], i[5])

    def delete_entry(self):
        pass

    def delete_table(self, table=""):
        if not table:
            table = self.table
        with self.db:
            self.cur.execute("DROP TABLE IF EXISTS {}".format(table))

    def delete_database(self):
        os.remove(self.db_file)


if __name__ == "__main__":
    c = Contacts()
    c.populate_database()
    c.show()
    c.insert("yes", "hey", "hey", "hey", "hey", "hey", "hey")