"""DemiMove

Usage:
    demimove [-d <dir>] [-c <file>] [-v...] [-q] [-h]

Options:
    -c, --config=<file>  Specify a config file to load.
    -d, --dir=<dir>      Specify a directory to load.
    -v                   Logging verbosity level, up to -vvv.
    -q, --quiet          Do not print logging messages to console.
    -h,  --help          Show this help text and exit.
    --version            Show the current DemiMove version.
"""
import logging
import re
import sys

from PyQt4 import QtGui, QtCore, uic


try:
    from docopt import docopt
except ImportError:
    print "ImportError: Please install docopt to use the CLI."


class DemiMove(QtGui.QMainWindow):

    def __init__(self, parent=None):

        super(DemiMove, self).__init__(parent)
        uic.loadUi("demimove.ui", self)

#         print self.mainsplitter.sizes()
        self.mainsplitter.setStretchFactor(0, 0)
        self.mainsplitter.setStretchFactor(1, 2)
#         print self.mainsplitter.sizes()

        self.setWindowIcon(QtGui.QIcon("icon.png"))

        self.create_dirtree()
        self.create_browsertree()
        log.error("initialized")
        sys.exit()

    def create_dirtree(self):
        self.dirmodel = QtGui.QFileSystemModel()
        self.dirmodel.setRootPath("")
        self.dirmodel.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.Hidden |
                                QtCore.QDir.NoDotAndDotDot)
        self.dirmodel.fileRenamed.connect(self.on_rootchange)
        self.dirmodel.rootPathChanged.connect(self.on_rootchange)
        self.dirmodel.directoryLoaded.connect(self.on_rootchange)

        self.dirtree.setModel(self.dirmodel)
        self.dirtree.setColumnHidden(1, True)
        self.dirtree.setColumnHidden(2, True)
        self.dirtree.setColumnHidden(3, True)


    def create_browsertree(self):
        self.browsermodel = QtGui.QFileSystemModel()
        self.browsermodel.setRootPath("")
        self.browsermodel.setFilter(QtCore.QDir.Dirs | QtCore.QDir.Files |
                                    QtCore.QDir.NoDotAndDotDot |
                                    QtCore.QDir.Hidden)

        self.browsertree.setModel(self.browsermodel)

    def on_rootchange(self, *args):
        print self.sender()


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


def configure_logger(loglevel=1, quiet=False):
    "Configures the logger (verbosity)."

    if loglevel > 3:
        loglevel = 3  # Cap at 3 to avoid index errors.
    levels = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
    log.setLevel(levels[loglevel])
    log.info("Loglevel is {}.".format(levels[loglevel]))

    if quiet:
        logging.disable(logging.ERROR)


def main():
    "Main entry point for DemiMove."
    app = QtGui.QApplication(sys.argv)
    browser = DemiMove()
    browser.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    log = create_logger()

    try:
        args = docopt(__doc__, version="0.1")
        configure_logger(args["-v"], args["--quiet"])
    except NameError:
        configure_logger(loglevel=2, quiet=False)
        log.error("Please install docopt to use the CLI.")

    main()
