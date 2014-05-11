import logging
import sys

def create_logger():
    "Creates the logger instance and adds handlers and formatting."
    log = logging.getLogger()
    logformat = "%(asctime)-14s %(levelname)-8s %(message)s"

    formatter = logging.Formatter(logformat)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    log.addHandler(console_handler)
    log.debug("Added logging console handler.")

    return log


def configure_logger(log, loglevel=1, quiet=False):
    "Configures the logger (verbosity)."

    if loglevel > 3:
        loglevel = 3  # Cap at 3 to avoid index errors.
    levels = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
    log.setLevel(levels[loglevel])
    log.info("Loglevel is {}.".format(levels[loglevel]))

    if quiet:
        logging.disable(logging.ERROR)
