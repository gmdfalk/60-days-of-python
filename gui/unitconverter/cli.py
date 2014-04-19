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

from docopt import docopt

from conversion import Data, Length, Volume


def main():
    args = docopt(__doc__, version="0.1")

    if not args["<args>"] or len(args["<args>"]) < 2:
        print "Not enough arguments."
        sys.exit(9)

    d = Data()
    data_units = {
                  d.bits: "bit bits",
                  d.bytes: "byte bytes",
                  d.kilobytes: "kb kilobytes kilobyte",
                  d.megabytes: "mb megabytes megabyte",
                  d.gigabytes: "gb gigabytes gigabyte",
                  d.terrabytes: "tb terrabytes terrabyte",
                  d.petabytes: "pb petabytes petabyte",
                  d.kibibytes: "kb kibibytes kibibyte",
                  d.mebibytes: "mb mebibytes mebibyte",
                  d.gibibytes: "gb gibibytes gibibyte",
                  d.tebibytes: "tb tebibytes tebibyte",
                  d.pebibytes: "pb pebibytes pebibyte"
                 }

    l = Length()
    length_units = {
                    l.millimeters: "mm millimeter millimeters",
                    l.centimeters: "cm centimeter centimeters",
                    l.meters: "m meter meters",
                    l.kilometers: "km kilometer kilometers",
                    l.inches: "in inches inch",
                    l.feet: "ft feet foot",
                    l.yards: "yd yard yards",
                    l.miles: "mi ml mile miles"
                    }


if __name__ == "__main__":
    main()
