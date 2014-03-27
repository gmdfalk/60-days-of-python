# coding: utf-8

import sqlite3 as lite

def insert(car_id, car, price):
    db = lite.connect('addresses.db')
    with db:
        cur = db.cursor()
        cur.execute("INSERT INTO Cars VALUES({}, '{}', {})".format(car_id, car, price))

# insert(1, "Audi", 5900000)

# Bogus list of addresses to work with.
addresses = (
    ("Max Demian", 60329, "Frankfurt", "Gutleutstraße 214", "069 741 382", "0176 241 332", "mikar@gmx.net"),
    ("Kristian Gottlieb", "", "Schellweiler", "Hardenbergerstr. 50", "06381 63 56 46", "212-660-2245", "K.Gottlieb@fake.de"),
    ("Mathias Hoover", 54340, "Schleich", "Güntzelstr. 12", "06507 58 02 52", "317 461 1232", "hoovercraft@lol.cat"),
    ("Dirk Vogt", 92303, "Neumarkt", "Luebecker Tordamm 1", "09181 75 77 80", "7024380985", "DirkVogt@armyspy.com"),
    ("Barbara Baier", 15230, "Frankfurt (Oder)", "Michaelkirchstr. 36", "05704 27 12 54", "1-323-472-0089", "bbaier@jourrapi.de"),
    ("Jens Kappel", 55481, "Schwarzen", "Joachimstaler Straße 97", "06763 39 39 51", "0700-413 22 5", "tinydancer@gmx.net"),
)

# Create and/or connect to our database.
db = lite.connect('addresses.db')

# Fix encoding issues.
db.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')

with db:

    cur = db.cursor()
    address = ("Max Demian", "63092", "Frankfurt", "Gutleutstraße 214",
               "069741382", "0176-241-332", "mikar@gmx.net")

    cur.execute("DROP TABLE IF EXISTS Addresses")
    cur.execute("CREATE TABLE Addresses(Name TEXT, ZIP Text, City Text, Street Text,\
                                   Phone Text, Mobile Text, Email TEXT)")
    cur.execute("INSERT INTO Addresses VALUES(?, ?, ?, ?, ?, ?, ?)", address)
    cur.execute("""SELECT * FROM Addresses""")
    next = cur.fetchone()
    for i in next: print i
