#!/usr/bin/env python2
"""UnitConverter (CLI)

Usage:
    cli.py <args>... [-d <decimals>] [-p <precision>] [h]

Options:
    -d, --decimals=<decimals>    Maximum decimal points. [default: 10]
    -p, --precision=<precision>  Accuracy of the floats. [default: 10]
    -h, --help                   Print this help text and exit.
    --version                    Show version of this CLI.

Examples:
    cli.py 10m to centimeter
    cli.py 10 meters to cm -d 3
    cli.py 10GB in bytes
    cli.py 10 liters oz
"""

import sys
import re

from docopt import docopt

from conversion import Data, Length, Volume


def check_data(arglist):
    d = Data()
    data_units = {
                  "bits": ["bit", "bits"],
                  "bytes": ["byte", "bytes"],
                  "kilobytes": ["kb", "kilobytes", "kilobyte"],
                  "megabytes": ["mb", "megabytes", "megabyte"],
                  "gigabytes": ["gb", "gigabytes", "gigabyte"],
                  "terrabytes": ["tb", "terrabytes", "terrabyte"],
                  "petabytes": ["pb", "petabytes", "petabyte"],
                  "kibibytes": ["kb", "kibibytes", "kibibyte"],
                  "mebibytes": ["mb", "mebibytes", "mebibyte"],
                  "gibibytes": ["gb", "gibibytes", "gibibyte"],
                  "tebibytes": ["tb", "tebibytes", "tebibyte"],
                  "pebibytes": ["pb", "pebibytes", "pebibyte"]
                 }

    # Abandon all hope, ye who enter here.
    found_units, found_count = [], 0
    for i in arglist:
        for k, v in data_units.items():
            try:
                v.index(i)
                found_units.append(k)
                found_count += 1
                if found_count == 2:
                    break
            except ValueError:
                pass
        if found_count == 2:
            break
    else:
        print "nothing found"
        return

    print found_count
    print found_units


def check_length(arglist):
    l = Length()
    length_units = {
                    l.millimeters: ["mm", "millimeter", "millimeters"],
                    l.centimeters: ["cm", "centimeter", "centimeters"],
                    l.meters: ["m", "meter", "meters"],
                    l.kilometers: ["km", "kilometer", "kilometers"],
                    l.inches: ["in", "inches", "inch"],
                    l.feet: ["ft", "feet", "foot"],
                    l.yards: ["yd", "yard", "yards"],
                    l.miles: ["mi", "ml", "mile", "miles"]
                    }


def check_volume(arglist):
    v = Volume()
    volume_units = {
                    v.milliliters: ["ml", "millimeter", "millimeters"],
                    v.centiliters: ["cl", "centiliter", "centiliters"],
                    v.liters: ["l", "liter", "liters"],
                    v.kiloliters: ["kl", "kiloliter", "kiloliters"],
                    v.ounces: ["oz", "floz ounce", "ounces"],
                    v.pints: ["pt", "pint", "pints"],
                    v.gallons: ["gal", "gallon", "gallons"],
                    v.barrels: ["bbl", "barrel", "barrels"]
                    }


def main():
    args = docopt(__doc__, version="0.1")

    # Preliminary input checks.
    arglist = [i.lower() for i in args["<args>"]]
    if not arglist or len(arglist) < 2:
        print "Not enough arguments."
        sys.exit(9)

    # Regex that splits the arglist into float/int and rest.
    rx = re.compile("(.?(?:\d+(?:\.\d+)?))(.*)")
    match = rx.search(" ".join(arglist))
    try:
        num, rest = match.group(1), match.group(2).split()
    except AttributeError:
        print "Invalid input! Need at least one float/integer."
        sys.exit(1)


    check_data(arglist)
    check_length(arglist)
    check_volume(arglist)


if __name__ == "__main__":
    main()
