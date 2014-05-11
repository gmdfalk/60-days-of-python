"""demimove

Usage:
    dmv <source> <target> [-s] [-f|-d] [-a] [-r] [-i|-p] [-n] [-c <n>] [-R]
        [-q] [-v...] [-h]

Arguments:
    source        Pattern to match (with globbing enabled by default).
                  With no other options set, this will match against all
                  non-hidden file and directory names in the current directory.
    target        Replacement pattern.

Options:
    -s, --simulate     Do a test run and dump the results to console.
    -f, --files        Only search file names. Default is both files and dirs.
    -d, --dirs         Only search directory names. Leaves files untouched.
    -a, --all          Include hidden files/directories.
    -r, --recursive    Apply changes recursively.
    -i, --interactive  Confirm before overwriting.
    -p, --prompt       Confirm any action.
    -n, --no-clobber   Do not overwrite an existing file.
    -c, --count=<n>    Increment a counter at the given index (0 start, -1 end)
    -R, --regex        Use regex matching instead of globbing.
    -q, --quiet        Do not print log messages to console.
    -v                 Logging verbosity, up to -vvv (debug).
    --version          Show the current demimove version.
    -h, --help         Show this help message and exit.

Examples:
    dmv "*.txt" "*.pdf" (will replace all .txt extensions with .pdf)
    dmv -f * season-* (will prepend "season-" to every file in the cwd)
"""
# TODO: History file and undo action?
import logging
import sys

import reporting


try:
    from docopt import docopt
except ImportError:
    print "Please install docopt first."
    sys.exit()


def main():
    args = docopt(__doc__, version="0.1")
    reporting.configure_logger(log, args["-v"], args["--quiet"])


if __name__ == "__main__":
    log = reporting.create_logger()
    main()
