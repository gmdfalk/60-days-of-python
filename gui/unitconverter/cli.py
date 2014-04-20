#!/usr/bin/env python2
"""UnitConverter (CLI)

Usage:
    cli.py <args>... [-d N] [-p N] [h]

Options:
    -d, --decimals=<decimals>    Maximum decimal points. [default: 10]
    -p, --precision=<precision>  Accuracy of the floats. [default: 10]
    -h, --help                   Print this help text and exit.
    --version                    Show version of this CLI.

Examples:
    cli.py 10m to centimeter
    cli.py 10 meters to cm -d 3
    cli.py 10GB in bytes
    cli.py 10 liters oz -p 80 -d 80
"""

import decimal
import re
import sys

from docopt import docopt

from conversion import Data, Length, Volume


def format_num(num):
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


def check_data(num, rest, decimals, precision):
    d = Data()
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

    # Abandon all hope, ye who enter here.
    found, found_count = [], 0
    for i in rest:
        for k, v in units.items():
            try:
                v.index(i)
                found.append(k)
                found_count += 1
                if found_count == 2:
                    break
            except ValueError:
                pass
        if found_count == 2:
            break
    else:
        return

    setattr(d, found[0], float(num))
    result = format_num(getattr(d, found[1]))
    # Trim the result to reflect the -d setting (number of decimal places).
    if "." in result:
        split = result.split(".")
        split[1] = split[1][:decimals]
        result = ".".join(split) if split[1] else split[0]
    print "{} {} are {} {}!".format(num, found[0], result, found[1])
    sys.exit()


def check_length(num, rest, decimals, precision):
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


def check_volume(num, rest, decimals, precision):
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

    # Regex that splits the arglist into float/int and rest. Allow leading dot.
    rx = re.compile("(.?(?:\d+(?:\.\d+)?))(.*)")
    match = rx.search(" ".join(arglist))
    try:
        num, rest = match.group(1), match.group(2).split()
    except AttributeError:
        print "Invalid input! Need at least one float/integer."
        sys.exit(1)

    # Set and/or correct decimal and precision options.
    try:
        decimals = int(args["--decimals"])
    except ValueError:
        decimals = 10
    try:
        precision = int(args["--precision"])
    except ValueError:
        precision = 10

    if decimals > 82:
        decimals = 82
    if precision > 82:
        precision = 82

    # The actual work happens here.
    check_data(num, rest, decimals, precision)
    check_length(num, rest, decimals, precision)
    check_volume(num, rest, decimals, precision)


if __name__ == "__main__":
    main()
