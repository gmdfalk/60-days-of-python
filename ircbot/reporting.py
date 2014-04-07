import time

class ChatLogger(object):
    "Only logs chat events"
    def __init__(self):
        self.logfiles = []

    def add_channel(self, chatlog):

        self.logfiles.append(chatlog)

    def log(self, msg, chatlog):
        "Write a log line with a timestamp to the channelfile"
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        chatlog.write("{} {}\n".format(timestamp, msg))
        chatlog.flush()

    def open_logs(self, channels, server):
        chatlogs = ["{}-{}.log".format(i, server) for i in channels]
        for chatlog in chatlogs:
            open(chatlog, "a")

    def close_logs(self):
        for i in self.logfiles:
            i.close_logs()
