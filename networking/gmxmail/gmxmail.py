#!/usr/bin/env python2
"""gmxmail

Usage:
    gmxmail [send <recipients> <message> [sign|encrypt|attach]] [--no-ssl]
            [-q] [-h] [-v...]
    gmxmail (add|del) <account> [<pgp-key>]

Arguments:
    get     Get mail. Optionally, specify the account to use with -a.
    send    Send a mail. Recipients comma-separated, message quoted.
    store   Store account information safely (address, password, pgp-key).

Options:
    -a, --acc=<acc>    Account to send the mail from. Asks for password if the
                       account hasn't been stored yet.
    --no-ssl           Do not secure connection with SSL/TLS.
    -h, --help         Show this help message and exit.
    -q, --quiet        Do not log bot events to stdout.
    -v                 Logging verbosity, up to -vvv.
"""
from getpass import getpass
import logging
import sys

from docopt import docopt


log = logging.getLogger("gmxmail")


def init_logging(loglevel, quiet):
    "Initializes the logger for system messages."
    logger = logging.getLogger()

    # Set the loglevel.
    if loglevel > 3:
        loglevel = 3
    levels = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
    logger.setLevel(levels[loglevel])

    logformat = "%(asctime)-14s %(levelname)-8s %(name)-8s %(message)s"

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


def get_mail():
    log.debug("get_mail")


def send_mail():
    log.debug("send_mail")


def store_acc(acc, pgpkey):
    password = getpass()
    log.debug(acc, password, pgpkey)


def main():
    args = docopt(__doc__, version="0.1")
    print args
    log.debug("test")
    init_logging(args["-v"], args["--quiet"])
    log.debug("test")
    if args["get"]:
        get_mail()
    elif args["send"]:
        send_mail()
    elif args["store"]:
        store_acc(args["<account>"], args["<pgp-key>"])

if __name__ == "__main__":
    main()
