#!/usr/bin/env python2
"""gmxmail

Usage:
    gmxmail [send <recipients> <message> [sign|encrypt|attach]] [-a <acc>]
            [-p <pass>] [--no-ssl] [-q] [-h] [-v...]

Arguments:
    send               Send a mail. Recipients comma-separated, message quoted.
                       Optionally, you can sign or encrypt the message (PGP).

Options:
    -a, --acc=<acc>    Account to send the e-mail from.
    -p, --pass=<pass>  Specify a password for the e-mail account.
    --no-ssl           Do not use SSL/TLS i.e. use an unsecure connection.
    -h, --help         Show this help message and exit.
    -q, --quiet        Do not log bot events to stdout. Will still log to file.
    -v                 Logging verbosity, up to -vvv.
"""

import ConfigParser
import logging
import sys

from docopt import docopt

from getmail import get_mail
from sendmail import send_mail


log = logging.getLogger("main")


def init_logging(loglevel, quiet):
    "Initializes the logger for system messages."
    logger = logging.getLogger()

    # Set the loglevel.
    if loglevel > 3:
        loglevel = 3
    levels = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
    logger.setLevel(levels[loglevel])

    logformat = "%(asctime)-14s %(levelname)-7s %(name)-5s %(message)s"

    formatter = logging.Formatter(logformat)

    # This discards all logging messages of ERROR and below.
#     logging.disable(logging.ERROR)
    # By default, we log to both file and stdout, unless quiet is enabled.
    if not quiet:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        log.info("Added logging console handler.")

    # If nologs is True, we do not log to any file.
    try:
        file_handler = logging.FileHandler("gmxmail.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        log.info("Added logging file handler.")
    except IOError:
        log.info("Could not attach file handler.")


def parse_opts(args):
    print args
    log.info("Parsing configuration file.")


def main():
    args = docopt(__doc__, version="0.1")
    # For now, set the loglevel always to debug.

    init_logging(args["-v"], args["--quiet"])

    parse_opts(args)
    if args["send"]:
        send_mail()
    else:
        get_mail()

if __name__ == "__main__":
    main()
