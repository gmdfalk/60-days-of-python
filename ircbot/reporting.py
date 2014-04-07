import time

class ChatLogger(object):
    "Only logs chat events"
    def __init__(self, server):
        self.logfiles = []
        self.server = server

    def add_channel(self, chatlog):

        self.logfiles.append(chatlog)

    def log(self, msg, channel):
        "Write a log line with a timestamp to the logfile of the channel"
        chatlog = "{}-{}.log".format(channel, self.server)
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        chatlog.write("{} {}\n".format(timestamp, msg))
        chatlog.flush()

    def open_logs(self, channels):
        chatlogs = ["{}-{}.log".format(i, self.server) for i in channels]
        for chatlog in chatlogs:
            chatlog = open(chatlog, "a")
            self.logfiles.append(chatlog)

    def close_logs(self):
        for i in self.logfiles:
            i.close()
