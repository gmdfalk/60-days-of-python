"""demimove

Usage:
    dmv [<source> [<target>]] [-D|-F] [-e <name>...] [-v|-vv|-vvv] [options]

Arguments:
    source        (Optional) Pattern to identify targets by.
                  Defaults to globbing but can be set to regular expression.
                  With no other options set, this will match against all
                  non-hidden file and directory names in the current directory.
    target        Optional replacement pattern for the source pattern.
                  For glob patterns, the number of wild cards has to match
                  those in the source pattern.

Options:
    -d, --dir=<path>      Specify the working directory. Otherwise cwd is used.
    -s, --simulate        Do a test run and dump the results to console.
    -D, --dirsonly        Only search directory names. Leaves files untouched.
    -F, --filesonly       Only search file names. Default is files + dirs.
    -e, --exclude=<n>...  Exclude files/directories. One or more instances.
    -a, --all             Include hidden files/directories.
    -k, --keep-extension  Preserve file extensions.
    -r, --recursive       Apply changes recursively.
    -i, --interactive     Confirm before overwriting.
    -p, --prompt          Confirm all rename actions.
    -n, --no-clobber      Do not overwrite an existing file.
    -R, --regex           Use regex matching instead of globbing.
    -c, --count=<N>       Increment a counter at the given index (-1 is end).
    -l, --lower           Change all letters to lowercase.
    -u, --upper           Change all letters to uppercase.
    -m, --media           Media mode: All lowercase, remove duplicate symbols,
                          replace spaces and similar actions.
    -v                    Logging verbosity, up to -vvv (debug).
    -q, --quiet           Do not print log messages to console.
    --version             Show the current demimove version.
    -h, --help            Show this help message and exit.

Examples:
    dmv "*.txt" "*.pdf" (will replace all .txt extensions with .pdf)
    dmv -f "*" "season-*" (will prepend "season-" to every file in the cwd)
"""
import sys

from fileops import FileOps


try:
    from docopt import docopt
except ImportError:
    print "Please install docopt first."
    sys.exit()


def main():
    args = docopt(__doc__, version="0.1")
    fileops = FileOps(dirsonly=args["--dirsonly"],
                      filesonly=args["--filesonly"],
                      recursive=args["--recursive"],
                      hidden=args["--all"],
                      simulate=args["--simulate"],
                      interactive=args["--interactive"],
                      prompt=args["--prompt"],
                      noclobber=args["--no-clobber"],
                      keepext=args["--keep-extension"],
                      count=args["--count"],
                      regex=args["--regex"],
                      quiet=args["--quiet"],
                      verbosity=args["-v"],
                      exclude=args["--exclude"])
    fileops.stage(args["<source>"], args["<target>"], args["--path"])


if __name__ == "__main__":
    main()
