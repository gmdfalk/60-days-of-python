import logging
import sys
import time

log = logging.getLogger("report")


class ChatLogger(object):
    "The logger for chat messages and urls"
    def __init__(self, server):
        self.logfiles = {}
        self.server = server

    def log(self, msg, channel):
        "Write a log line with a timestamp to the logfile of the channel"
        timestamp = time.strftime("%H:%M:%S", time.localtime(time.time()))
        self.logfiles[channel].write("[{}] {}\n".format(timestamp, msg))
        self.logfiles[channel].flush()

    def log_url(self, msg, channel):
        "Messages that contain urls are logged separately. Why not?"
        timestamp = time.strftime("%H:%M:%S", time.localtime(time.time()))
        self.logfiles["urls"].write("[{}] ({}) {}\n".format(timestamp,
                                                            channel, msg))
        self.logfiles["urls"].flush()

    def add_channel(self, channel):
#         channel = channel.strip("#")  # I hate escape characters.
        if channel not in self.logfiles:
            self.logfiles[channel] = open("logs/{}-{}.log"
                                          .format(channel, self.server), "a")
        else:
            # Track redundant channel additions here.
            log.debug("Tried to add an existing channel: {}".format(channel))

    def del_channel(self, channel):
        "Removes a channel from the logfiles dictionary"
        # To avoid a keyerror, pop will return None if the key is not found.
        self.logfiles.pop(channel, None)

    def open_logs(self, channels):
        for channel in channels:
            self.add_channel(channel)
        self.logfiles["urls"] = open("logs/urls-{}.log"
                                     .format(self.server), "a")

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
#     s = "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"

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

        file_handler = logging.FileHandler(logfile)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
