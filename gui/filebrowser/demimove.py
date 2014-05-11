"""demimove

Usage:
    dmv <source> <target> [-a <adm>] [-f] [-d] [-r] [-R] [-t] [-c]
        [-q] [-v...] [-h]

Arguments:
    source        a
    target        b

Options:
    -r, --recursive   Apply changes recursively.
    -R, --regex       Use regex matching instead of globbing.
    -c, --confirm     Confirm overwrite actions.
    -t, --test        Do a test run and dump the results to console.
    -h, --help        Show this help message and exit.
    -q, --quiet       Do not print log messages to console.
    -v                Logging verbosity, up to -vvv.
"""
import logging
import shutil
import sys

import reporting


try:
    from docopt import docopt
except:
    print "Please install docopt first."
    sys.exit()


def main():
    args = docopt(__doc__, version="0.1")
    reporting.configure_logger(log, args["-v"], args["--quiet"])


if __name__ == "__main__":
    log = reporting.create_logger()
    main()
