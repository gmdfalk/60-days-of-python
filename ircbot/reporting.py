import time
import logging

log = logging.getLogger("reporting")

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
        if channel in self.logfiles:
            # FIXME: Where do the attempted duplicate dict entries come from?
            print "been here before"
        else:
            self.logfiles[channel] = open("logs/{}-{}.log"
                                      .format(channel, self.server), "a")

    def open_logs(self, channels):
        for channel in channels:
            self.add_channel(channel)
        self.logfiles["urls"] = open("logs/urls-{}.log"
                                     .format(self.server), "a")

    def close_logs(self):
        for i in self.logfiles.values():
            i.close()
        self.logfiles = {}
