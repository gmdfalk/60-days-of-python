import logging
import sys
import time


class ChatLogger(object):
    "Logs chat messages only"
    def __init__(self, server):
        self.logfiles = {}
        self.server = server

    def log(self, msg, channel):
        "Write a log line with a timestamp to the logfile of the channel"
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        self.logfiles[channel].write("{} {}\n".format(timestamp, msg))
        self.logfiles[channel].flush()

    def log_url(self, url):
        self.logfiles["urls"].write("{}\n".format(url))
        self.logfiles["urls"].flush()

    def add_channel(self, channel):
#         channel = channel.strip("#")  # I hate escape characters.
        if channel not in self.logfiles:
            self.logfiles[channel] = open("logs/{}-{}.log"
                                          .format(channel, self.server), "a")
        else:
            # FIXME: Where do the attempted duplicate dict entries come from?
            pass

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


def init_logging(level):
    "Initializes the logger for system messages (to stdout only, currently)"
    logger = logging.getLogger()

    levels = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG][::-1]
    logger.setLevel(levels[level])

    default = "%(asctime)-15s %(levelname)-8s %(name)-11s %(message)s"
    formatter = logging.Formatter(default)
    # Append file name + number if debug is enabled

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
