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

import decimal
import re
import sys

from docopt import docopt

from conversion import Data, Length, Volume


def format_num(num):
    "Format a number into a nicer format, i.e. strip trailing 0s, dots etc."
    try:
        dec = decimal.Decimal(num)
    except:
        return "bad"
    tup = dec.as_tuple()
    delta = len(tup.digits) + tup.exponent
    digits = "".join(str(d) for d in tup.digits)
    if delta <= 0:
        zeros = abs(tup.exponent) - len(tup.digits)
        val = "0." + ("0" * zeros) + digits
    else:
        val = digits[:delta] + ("0" * tup.exponent) + "." + digits[delta:]
    val = val.rstrip("0")
    if val[-1] == ".":
        val = val[:-1]
    if tup.sign:
        return "-" + val
    return val


class CLIConverter(object):

    def __init__(self):
        "Read command-line arguments, assign to self and start the conversion."
        args = docopt(__doc__, version="0.1")

        # Preliminary input checks.
        arglist = [i.lower() for i in args["<args>"]]
        if not arglist or len(arglist) < 2:
            print "Not enough arguments."
            sys.exit(9)

        # Regex that splits the arglist into a number and the rest of the args.
        rx = re.compile("(.?(?:\d+(?:\.\d+)?))(.*)")
        match = rx.search(" ".join(arglist))
        try:
            self.num, self.rest = match.group(1), match.group(2).split()
        except AttributeError:
            print "Invalid input! Need at least one float/integer."
            sys.exit(1)

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
                        "yards": ["yd", "yard", "yards"],
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
                        "ounces": ["oz", "floz ounce", "ounces"],
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
                    pass
        # Check found for duplicates but preserve the order.
        seen = set()
        seen_add = seen.add
        found = [i for i in found if i not in seen and not seen_add(i)]
        # If we haven't found 2 matching types, exit here.
        if len(found) < 2:
            return

        unit.precision = self.precision
        setattr(unit, found[0], float(self.num))
        result = format_num(getattr(unit, found[1]))
        # Trim the result to reflect the -d setting (number of decimal places).
        if "." in result:
            split = result.split(".")
            split[1] = split[1][:self.decimals]
            result = ".".join(split) if split[1] else split[0]
        print "{} {} are {} {}!".format(self.num, found[0], result, found[1])
        sys.exit()


if __name__ == "__main__":
    c = CLIConverter()
