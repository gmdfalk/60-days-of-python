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
        # TODO: Fix encoding issues. I will have to revisit this as it doesn't
        # seem right.
        self.db.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')

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
            cur = self.db.cursor()
            cur.execute("DROP TABLE IF EXISTS {}".format(self.table))
            cur.execute("CREATE TABLE {}(Name TEXT, Zip Text, City Text,\
                              Street Text, Phone Text, Mobile Text,\
                              Email TEXT)".format(self.table))
            cur.executemany("INSERT INTO {} VALUES(?, ?, ?, ?, ?, ?, ?\
                                 )".format(self.table), addresses)

    def insert(self, name="", zipcode="", city="", street="",
               phone="", mobile="", email="", table=None):
        "Insert a new entry into the database in the selected table"
        if table is None:
            table = self.table
        with self.db:
            cur = self.db.cursor()
            cur.execute("INSERT INTO {} VALUES(?, ?, ?, ?, ?, ?, ?)\
                             ".format(table), (name, zipcode, city, street,
                                               phone, mobile, email))

    def show_all(self, table=None):
        "Print out all contacts of the currently selected table"
        if table is None:
            table = self.table
        # FIXME: SQLite wants to use ASCII here so we abide, for now.
        with self.db:
            cur = self.db.cursor()
            self.db.text_factory = str
            cur.execute("SELECT * FROM {}".format(table))
            for i in cur.fetchall():
                print "{}, {} {}, {}".format(i[0], i[1], i[2], i[3])
                print "{}, {}, mobile: {}\n".format(i[6], i[4], i[5])
            self.db.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')

    def delete_table(self, table=None):
        if table is None:
            table = self.table
        with self.db:
            cur = self.db.cursor()
            cur.execute("DROP TABLE IF EXISTS {}".format(table))

    def delete_database(self, db_file=None):
        if db_file is None:
            db_file = self.db_file
        # FIXME: Somehow, when testing this method, the db_file gets deleted
        # before we even get to the next line. Maybe tearDown interfering?
        try:
            os.remove(db_file)
        except OSError as e:
            print e

    def search(self, search_string, table=None):
        if table is None:
            table = self.table
        columns = "Name, Zip, City, Street, Phone, Mobile, Email"
        with self.db:
            cur = self.db.cursor()
            # Brace yourselves. Long lines are coming.
            results = []
            for col in columns.split(","):
                for row in cur.execute("SELECT {} FROM {} WHERE {} LIKE ?".format(
                    columns, table, col), ('%{}%'.format(search_string),)):
                    if row:
                        results.append(row)
            return results


# if __name__ == "__main__":
#     c = Contacts()
#     c.populate_database()
#     c.show_all()
#     c.insert(name="Lisa Simpson", zipcode="80085", city="Springfield",
#              street="742 Evergreen Terrace", phone="555 636", mobile="",
#              email="chunkylover53@aol.com")
#     c.search("Simpson")
