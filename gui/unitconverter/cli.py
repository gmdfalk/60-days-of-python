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

from docopt import docopt

from conversion import Data, Length, Volume


def main():
    args = docopt(__doc__, version="0.1")

    bytes = ["byte", "bytes", "Byte", "Bytes"]
    bits = ["bit", "bits", ""]

    for i in args["<args>"]:
        # find source
        # find target
        # convert and return
        pass

if __name__ == "__main__":
    main()
