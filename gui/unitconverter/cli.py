#!/usr/bin/env python2
"""UnitConverter (CLI)

Usage:
    cli.py (<args>...|<args> <obase> [-i N]) [-d N] [h]

Options:
    -i, --ibase=N      Input base for number conversion. [default: 10]
    -o, --obase=N      Output base for number conversion. [default: 10]
    -d, --decplaces=N  Number of decimal places. [default: 10]
    -h, --help         Print this help text and exit.
    --version          Show the version of UnitConverter.

Examples:
    cli.py 10m to centimeter
    cli.py 10 meters in Cm -d 3
    cli.py 10.9in oz
"""
# TODO: Positional awareness for number arguments.
from string import digits, punctuation
import re
import sys

from docopt import docopt

from conversion import Base, Data, Length, Volume, Weight


class CLIConverter(object):

    def __init__(self):
        "Read command-line arguments, assign to self and start the conversion."
        args = docopt(__doc__, version="0.1")
        print args

        # Correct the base:
        for i in (args["--obase"], args["--ibase"]):
            if i < 2 or i > 64:
                print "Invalid base ({}). Valid range is 2-64.".format(i)
                sys.exit(1)

        # Preliminary input checks.
        arglist = [i.lower() for i in args["<args>"]]
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
        self.decplaces = int(args["--decplaces"])

        # Initialize the checks.
        self.check_base()
        self.check_data()
        self.check_volume()
        self.check_length()
        self.check_weight()

        # If we arrive here, we didn't get any results.
        print "Sorry, could not find two matching measurement units."
        sys.exit(1)

    def check_base(self):

        unittype = Base()
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

        self.try_conversion(unittype, units)

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

        self.try_conversion(unittype, units)


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

        self.try_conversion(unittype, units)


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

        self.try_conversion(unittype, units)

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

        self.try_conversion(unittype, units)


    def try_conversion(self, unittype, units):
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
