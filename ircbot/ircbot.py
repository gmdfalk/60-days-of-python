#!/usr/bin/env python2
"""IRCBot (Quizzing, Logging, ...)

Usage:
    bot.py [-h] [-s <server>] [-p <port>] [--password=<pass>] [-c <channel>...]
           [-n <nick>] [-o <output>]  [--max-tries N] [-v N] [-q]

Options:
    -s, --server=<server>    DNS address [default: irc.freenode.net]
    -p, --port=<port>        Port number of the IRC server [default: 6667]
    -pw, --password=<pass>   Server password, if required
    -c, --channel=<channel>  IRC Channel to join [default: #maxtest]
    -n, --nick=<nick>        Nickname of the bot [default: maxbot]
    -o, --output=<output>    Logging file [default: stdout]
    --max-tries N            Limit retries on network errors [default: 4]
    -h, --help               Show this help message and exit
    -v, --verbose N          Verbose logging (0-3) [default: 1]
    -q, --quiet              Quiet logging
"""

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log
from docopt import docopt

import time
import sys
import logging


class MessageLogger(object):

    def __init__(self, file):
        self.file = file

    def log(self, message):
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        self.file.write("{} {}\n".format(timestamp, message))
        self.file.flush()

    def close(self):
        self.file.close()


class LogBot(irc.IRCClient):

    nickname = "maxbot"

    def connection_made(self):
        now = time.asctime(time.localtime(time.time()))
        irc.IRCClient.connectionMade(self)
        self.logger = MessageLogger(open(self.factory.filename, "a"))
        self.logger.log("[connected at {}]".format(now))

    def connection_lost(self, reason):
        now = time.asctime(time.localtime(time.time()))
        irc.IRCClient.connectionLost(self, reason)
        self.logger.log("[disconnected at {}]".format(now))
        self.logger.close()

    def signed_on(self):
        self.join(self.factory.channel)

    def joined(self, channel):
        self.logger.log("[I have joined {}".format(channel))


    def privmsg(self, user, channel, msg):
        user = user.split("!", 1)[0]
        self.logger.log("<{}> {}".format(user, msg))

        # Check to see if they're sending me a private message
        if channel == self.nickname:
            msg = "It isn't nice to whisper! Play nice with the group."
            self.msg(user, msg)
            return

        if msg.startswith(self.nickname + ":"):
            msg = "{}: I am a log bot".format(user)
            self.msg(channel, msg)
            self.logger.log("<{}> {}".format(self.nickname, msg))


    def action(self, user, channel, msg):
        user = user.split("!", 1)[0]

class Empty(object):
    pass

def main():
    "Parse arguments, set up event loop, run crawler and print a report."

    levels = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
    if args["--quiet"]:
        logging.basicConfig(level=levels[0])
    else:
        logging.basicConfig(level=levels[int(args["--verbose"])])

    # Instantiating the crawler with our arguments.
    bot = Empty(server=args["--server"],
                port=args["--port"],
                channel=args["--channel"],
                nick=int(args["--nick"]),
                output=int(args["--output"]),
                max_tries=int(args["--max-tries"])
                )

    # "And this is where the magic happens."
#     try:
#         loop.run_until_complete(crawler.crawl())
#     except KeyboardInterrupt:
#         sys.stderr.flush()
#         print('\nInterrupted\n')
#     finally:
#         reporting.report(crawler)
#         crawler.close()
#         loop.close()


if __name__ == "__main__":
    args = docopt(__doc__, version="0.1")
    print args
#     main()
