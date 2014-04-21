#!/usr/bin/env python2
"""UnitConverter (CLI)

Usage:
    cli.py <args>... [-d <decimals>] [-p <precision>] [h]

Options:
    -d, --decimals=<decimals>    Maximum decimal points. Max 82. [default: 10]
    -p, --precision=<precision>  Accuracy of the floats. Max 82. [default: 10]
    -h, --help                   Print this help text and exit.
    --version                    Show the version of UnitConverter.

Examples:
    cli.py 10m to centimeter
    cli.py 10Liters ounce -p 80 -d 80
    cli.py 10 meters to cm -d 3
"""
# TODO: Positional awareness for number arguments.
from string import digits, punctuation
import re
import sys

from docopt import docopt

from conversion import Data, Length, Volume


class CLIConverter(object):

    def __init__(self):
        "Read command-line arguments, assign to self and start the conversion."
        args = docopt(__doc__, version="0.1")

        # Preliminary input checks.
        arglist = [i.lower() for i in args["<args>"]]
        if not arglist or len(arglist) < 2:
            print "Not enough arguments."
            sys.exit(9)

        # Extract a number (float/int) from the arglist. Allows leading dot.
        rx = re.compile("\d+(?:\.\d+)?|\.\d+")
        match = rx.search(" ".join(arglist))
        try:
            self.num = match.group()
        except AttributeError:
            print "Invalid input! Need at least one float/integer."
            sys.exit(1)
        print self.num
        # FIXME: If i strip the number here I can't allow (silly) searches
        # like "how many cm are 5 m.". Needs positional awareness, see top TODO
        self.rest = [i.strip(digits + punctuation) for i in arglist]
        print self.rest
        # Set and/or correct decimal and precision options.
        try:
            self.decimals = int(args["--decimals"])
        except ValueError:
            self.decimals = 10
        try:
            self.precision = int(args["--precision"])
        except ValueError:
            self.precision = 10

        if self.decimals > 82:
            self.decimals = 82
        if self.precision > 82:
            self.precision = 82

        # Initialize the checks.
        self.check_data()
        self.check_volume()
        # Check length last because it has "in" which can cause problems for
        # searches like "100 liters in ml" if ml were a valid length unit.
        self.check_length()
        print "Sorry, could not find two matching measurement units."
        sys.exit(1)

    def check_data(self):
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

        unit = Data()
        self.try_conversion(unit, units)


    def check_length(self):
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
        unit = Length()
        self.try_conversion(unit, units)


    def check_volume(self):
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

        unit = Volume()
        self.try_conversion(unit, units)


    def try_conversion(self, unit, units):
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

        unit.precision = self.precision
        setattr(unit, found[0], float(self.num))
        result = getattr(unit, found[1])
        print "{} {} are {} {}!".format(self.num, found[0], result, found[1])
        sys.exit()


if __name__ == "__main__":
    c = CLIConverter()
