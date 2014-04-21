#!/usr/bin/env python2
"""UnitConverter (CLI)

Usage:
    cli.py <args>... [-d N] [h]
    cli.py base <num> <ibase> [<obase>] [h]
    cli.py rot <msg>... [-s N] [h]

Options:
    -d, --decimals=N  Number of decimal places. [default: 10]
    -s, --shift=N     Caesar cipher shift. [default: 13]
    -h, --help        Print this help text and exit.
    --version         Show the version of UnitConverter.

Examples:
    cli.py 10.4m in km
    cli.py -d 30 100 meters inch
    cli.py rot this is the message -s 10
    cli.py base "100" 2 16 (NYI, this would convert binary 100 to hex)
"""
from string import digits, punctuation
import re
import sys

from docopt import docopt

from conversion import Base, Data, Length, Volume, Weight, rot


class CLIConverter(object):

    def __init__(self):
        "Read command-line arguments, assign to self and start the conversion."
        self.args = docopt(__doc__, version="0.1")

        if self.args["rot"]:
            self.start_caesar_conversion()
        elif self.args["base"]:
            pass
        else:
            self.start_unit_conversion()

    def start_caesar_conversion(self):
        msg = " ".join(self.args["<msg>"])
        shift = int(self.args["--shift"])
        print rot(msg, shift)

    def start_unit_conversion(self):
        # Preliminary input checks.
        arglist = [i.lower() for i in self.args["<args>"]]
        if not arglist or len(arglist) < 2:
            print "Not enough arguments."
            sys.exit(9)

        # Match the first number(int/float) in the arglist. Allows leading dot.
        rx = re.compile("\d+(?:\.\d+)?|\.\d+")
        match = rx.search(" ".join(arglist))
        try:
            self.num = match.group()
        except AttributeError:
            print "Invalid input! Need at least one float/integer."
            sys.exit(1)

        self.rest = [i.strip(digits + punctuation) for i in arglist]
        self.decplaces = int(self.args["--decimals"])

        # Initialize the checks.
        self.check_data()
        self.check_volume()
        self.check_length()
        self.check_weight()

        # If we arrive here, we didn't get any results.
        print "Sorry, could not find two matching measurement units."
        sys.exit(1)

    def check_data(self):

        unittype = Data()
        units = {
                  "bits": ["bit", "bits"],
                  "bytes": ["byte", "bytes"],
                  "kilobytes": ["kb", "kilobytes", "kilobyte"],
                  "megabytes": ["mb", "megabytes", "megabyte"],
                  "gigabytes": ["gb", "gigabytes", "gigabyte"],
                  "terrabytes": ["tb", "terrabytes", "terrabyte"],
                  "petabytes": ["pb", "petabytes", "petabyte"],
                  "kibibytes": ["kib", "kibibytes", "kibibyte"],
                  "mebibytes": ["mib", "mebibytes", "mebibyte"],
                  "gibibytes": ["gib", "gibibytes", "gibibyte"],
                  "tebibytes": ["tib", "tebibytes", "tebibyte"],
                  "pebibytes": ["pib", "pebibytes", "pebibyte"]
                 }

        self.convert_unit(unittype, units)


    def check_length(self):

        unittype = Length()
        units = {
                        "millimeters": ["mm", "millimeter", "millimeters"],
                        "centimeters": ["cm", "centimeter", "centimeters"],
                        "meters": ["m", "meter", "meters"],
                        "kilometers": ["km", "kilometer", "kilometers"],
                        "inches": ["in", "inches", "inch"],
                        "feet": ["ft", "feet", "foot"],
                        "yards": ["yd", "yds", "yard", "yards"],
                        "miles": ["mi", "mile", "miles"]
                        }

        self.convert_unit(unittype, units)


    def check_volume(self):

        unittype = Volume()
        units = {
                        "milliliters": ["ml", "milliliter", "milliliters"],
                        "centiliters": ["cl", "centiliter", "centiliters"],
                        "liters": ["l", "liter", "liters"],
                        "kiloliters": ["kl", "kiloliter", "kiloliters"],
                        "ounces": ["oz", "floz", "ounce", "ounces"],
                        "pints": ["pt", "pint", "pints"],
                        "gallons": ["gal", "gallon", "gallons"],
                        "barrels": ["bbl", "barrel", "barrels"]
                        }

        self.convert_unit(unittype, units)

    def check_weight(self):

        unittype = Weight()
        units = {
                        "milligrams": ["mg", "milligram", "milligrams"],
                        "grams": ["g", "gram", "grams"],
                        "kilograms": ["kg", "kilogram", "kilograms"],
                        "tons": ["t", "ton", "tons"],
                        "drams": ["dr", "dram", "drams"],
                        "ounces": ["oz", "ounce", "ounces"],
                        "pounds": ["lb", "lbs", "pound", "pounds"],
                        "ustons": ["ust", "ustons", "us tons"]
                        }

        self.convert_unit(unittype, units)


    def convert_unit(self, unittype, units):
        """The main loop. Tries to find 2 measurement units of the same type.
        If it finds those, it will print a conversion result and exit."""
        found = []
        for i in self.rest:
            for k, v in units.items():
                try:
                    v.index(i)
                    found.append(k)
                except ValueError:
                    continue

        # Check found for duplicates but preserve the order.
        seen = set()
        seen_add = seen.add
        found = [i for i in found if i not in seen and not seen_add(i)]
        # If we haven't found 2 matching types, exit here.
        if len(found) < 2:
            return
        # OTOH, if we have more than 2 results, get rid of troublemakers.
        # FIXME: hacky.
        elif len(found) > 2 and "inches" in found:
            del found[found.index("inches")]

        unittype.decplaces = self.decplaces
        setattr(unittype, found[0], float(self.num))
        result = getattr(unittype, found[1])
        print "{} {} are {} {}!".format(self.num, found[0], result, found[1])
        sys.exit()


if __name__ == "__main__":
    c = CLIConverter()
