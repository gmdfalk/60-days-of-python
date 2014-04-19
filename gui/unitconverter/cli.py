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

d = Data()
data_units = {
              d.bits: "bit bits",
              d.bytes: "byte bytes",
              d.KB: "kb kilobytes kilobyte",
              d.MB: "mb megabytes megabyte",
              d.GB: "gb gigabytes gigabyte",
              d.TB: "tb terrabytes terrabyte",
              d.PB: "pb petabytes petabyte",
              d.KiB: "kb kibibytes kibibyte",
              d.MiB: "mb mebibytes mebibyte",
              d.GiB: "gb gibibytes gibibyte",
              d.TiB: "tb tebibytes tebibyte",
              d.PiB: "pb pebibytes pebibyte"
             }
l = Length()
length_units = {
                l.mm: "mm millimeter millimeters",
                l.cm: "cm centimeter centimeters",

                }

def check_validity(args):
    if not args or len(args) < 2:
        print "Not enough arguments."
        sys.exit(9)


def main():
    args = docopt(__doc__, version="0.1")

    check_validity(args["<args>"])
    for i in args["<args>"]:
#         check_validity(args)
        # find source
        # find target
        # convert and return
        pass

if __name__ == "__main__":
    main()
