import time

class ChatLogger(object):
    "Only logs chat events"
    def __init__(self, server):
        self.logfiles = {}
        self.server = server

    def log(self, msg, channel):
        "Write a log line with a timestamp to the logfile of the channel"
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        self.logfiles[channel].write("{} {}\n".format(timestamp, msg))
        self.logfiles[channel].flush()

    def add_channel(self, channel):
        if channel in self.logfiles:
            print channel, "already exists:", self.logfiles[channel]
        self.logfiles[channel] = open("{}-{}.log".format(channel,
                                                         self.server), "a")

    def open_logs(self, channels):
        for channel in channels:
            self.add_channel(channel)

    def close_logs(self):
        for i in self.logfiles.values():
            i.close()
        self.logfiles = {}
