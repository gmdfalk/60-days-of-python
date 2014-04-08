import logging
import sys
import time


log = logging.getLogger("report")


class ChatLogger(object):
    "The logger for chat messages and URLs"
    def __init__(self, factory):
        self.logfiles = {}
        self.factory = factory
        self.server = self.factory.network_name
        self.prefix = "logs/"  # Path goes here.
        self.suffix = ".log"

    def log(self, msg, channel):
        "Write a log line with a time stamp to the logfile of the channel"
        timestamp = time.strftime("%H:%M:%S", time.localtime(time.time()))
        try:
            self.logfiles[channel].write("[{}] {}\n".format(timestamp, msg))
            self.logfiles[channel].flush()
        except KeyError as e:
            log.error("KeyError: {}. Missing write permissions?".format(e))
            if self.factory.logs_enabled:
                self.factory.logs_enabled = False

    def log_url(self, msg, channel):
        "Messages that contain urls are logged separately. Why not?"
        timestamp = time.strftime("%H:%M:%S", time.localtime(time.time()))
        self.logfiles["urls"].write("[{}] ({}) {}\n".format(timestamp,
                                                            channel, msg))
        self.logfiles["urls"].flush()

    def add_channel(self, channel):
#       channel = channel.strip("#")  # I hate escape characters.
        try:
            if channel not in self.logfiles:
                self.logfiles[channel] = open("{}{}-{}{}" .format(self.prefix,
                                              channel, self.server, self.suffix),
                                              "a")
        except IOError as e:
            err_str = "IOError: Disabling chatlogs. Missing write permissions?"
            log.error("{}".format(e))
            if self.factory.logs_enabled:
                self.factory.logs_enabled = False
                log.error("{}".format(err_str))

    def del_channel(self, channel):
        "Removes a channel from the logfiles dictionary"
        # To avoid a keyerror, pop will return None if the key is not found.
        self.logfiles.pop(channel, None)

    def open_logs(self, channels):
        try:
            for channel in channels:
                self.add_channel(channel)

            self.logfiles["urls"] = open("{}urls-{}{}".format(self.prefix,
                                         self.server, self.suffix), "a")
        except IOError as e:
            return

    def close_logs(self):
        for i in self.logfiles.values():
            i.close()
        self.logfiles = {}


def init_syslog(logfile, loglevel, nologs, quiet):
    "Initializes the logger for system messages"
    logger = logging.getLogger()

    # Set the loglevel.
    levels = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
    logger.setLevel(levels[loglevel])

    logformat = "%(asctime)-14s %(levelname)-8s %(name)-8s %(message)s"

    formatter = logging.Formatter(logformat)

    # If nologs is True, we do not log anything.
    if nologs:
        # This discards all logging messages of ERROR and below.
        logging.disable(logging.ERROR)
    else:
        # By default, we log to both file and stdout, unless quiet is enabled.
        if not quiet:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
            log.debug("Added logging console handler.")

        try:
            file_handler = logging.FileHandler(logfile)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            log.debug("Added logging file handler.")
        except IOError:
            log.error("Could not attach file handler. Only logging to stdout.")
