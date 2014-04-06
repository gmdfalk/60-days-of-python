import time

class ChatLogger(object):
    """
    An independent logger class (because separation of application
    and protocol logic is a good thing).
    """
    def __init__(self, logfile):
        self.logfile = logfile

    def log(self, msg):
        """Write a log line to the file with timestamp."""
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        self.logfile.write("{} {}\n".format(timestamp, msg))
        self.logfile.flush()

    def close(self):
        self.logfile.close()