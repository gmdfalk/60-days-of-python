"""demimove

Usage:
    dmv <source> <target> [-s] [-f|-d] [-a] [-r] [-i|-p] [-n] [-R]
        [-c <n>] [-e <e>...] [-v...] [-q] [-h]

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
    -e, --exclude=<e>  Exclude files/directories. Space separated.
    -r, --recursive    Apply changes recursively.
    -i, --interactive  Confirm before overwriting.
    -p, --prompt       Confirm any action.
    -n, --no-clobber   Do not overwrite an existing file.
    -R, --regex        Use regex matching instead of globbing.
    -c, --count=<n>    Increment a counter at the given index (0 start, -1 end)
    -v                 Logging verbosity, up to -vvv (debug).
    -q, --quiet        Do not print log messages to console.
    --version          Show the current demimove version.
    -h, --help         Show this help message and exit.

Examples:
    dmv "*.txt" "*.pdf" (will replace all .txt extensions with .pdf)
    dmv -f "*" "season-*" (will prepend "season-" to every file in the cwd)
"""
import os
import sys

from fileops import FileOps
import reporting


try:
    from docopt import docopt
except ImportError:
    print "Please install docopt first."
    sys.exit()


def main():
    fileops = FileOps()
    print args


if __name__ == "__main__":
    log = reporting.create_logger()
    args = docopt(__doc__, version="0.1")
    reporting.configure_logger(log, args["-v"], args["--quiet"])
    main()
