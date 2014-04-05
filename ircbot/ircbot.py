#!/usr/bin/env python2
"""IRCBot

Usage:
    ircbot.py [-h] [-s <server>] [-p <port>] [--password=<pass>] [-c <channel>]
              [-n <nick>] [-o <file>]  [--max-tries N] [-v N] [-q]

Options:
    -s, --server=<server>    DNS address [default: irc.freenode.net]
    -p, --port=<port>        Port number of the IRC server [default: 6667]
    -pw, --password=<pass>   Server password, if required
    -c, --channel=<channel>  Channels, comma separated [default: maxtest]
    -n, --nick=<nick>        Nickname of the bot [default: maxbot]
    -o, --output=<file>      Logging file [default: test.log]
    --max-tries N            Limit retries on network errors [default: 4]
    -h, --help               Show this help message and exit
    -v, --verbose N          Verbose logging (0-3) [default: 1]
    -q, --quiet              Quiet logging
"""

# Possible features:
# HTTP link capture/collection and saving or displaying the title in chat
# Weather and date/time information (day + week number, too)
# Quiz
# Collecting/displaying quotes (Chirpy?)
# Store notes with keyword and repeat them on demand
# Google search (or other services, like translate)
# Operator/Auth features (Kick, Ban, automatically give OP)
# Disable/enable commands, public ignore
# Fortune cookies or something like that
# Seen (track last message by user x)
# Conduct a poll.
# Evaluate python/bash
# Dictionary, wiki
# Search channel log.
# Message system (leaving a notification)


from twisted.internet import defer, endpoints, protocol, reactor, task
from twisted.words.protocols import irc
from twisted.python.logfile import DailyLogFile
from twisted.python import log
from docopt import docopt
import sys


class Protocol(irc.IRCClient):

    def __init__(self, nickname):
        self.deferred = defer.Deferred()
        self.nickname = nickname

#     def connectionMade(self):
#         log.msg("Connected.")

    def connectionLost(self, reason):
#         log.msg("Connection lost:", reason)
#         self.deferred.errback(reason)
        irc.IRCClient.connectionLost(self, reason)

    def irc_ERR_NICKNAMEINUSE(self, prefix, params):
        print prefix
        print params

    def signedOn(self):
        # This is called once the server has acknowledged that we sent
        # both NICK and USER.
        for channel in self.factory.channels:
            self.join(channel)

#     def joined(self, channel):
#         log.msg("Joined channel:", channel)

    # Obviously, called when a PRIVMSG is received.
    def privmsg(self, user, channel, message):
        nick, _, host = user.partition("!")
        message = message.strip()
        if not message.startswith("!"):  # not a trigger command
            return  # so do nothing
        command, sep, rest = message.lstrip("!").partition(" ")
        # Get the function corresponding to the command given.
        func = getattr(self, "command_" + command, None)
        # Or, if there was no function, ignore the message.
        if func is None:
            return
        # maybeDeferred will always return a Deferred. It calls func(rest), and
        # if that returned a Deferred, return that. Otherwise, return the
        # return value of the function wrapped in
        # twisted.internet.defer.succeed. If an exception was raised, wrap the
        # traceback in twisted.internet.defer.fail and return that.
        d = defer.maybeDeferred(func, rest)
        # Add callbacks to deal with whatever the command results are.
        # If the command gives error, the _show_error callback will turn the
        # error into a terse message first:
        d.addErrback(self._showError)
        # Whatever is returned is sent back as a reply:
        if channel == self.nickname:
            # When channel == self.nickname, the message was sent to the bot
            # directly and not to a channel. So we will answer directly too:
            d.addCallback(self._sendMessage, nick)
        else:
            # Otherwise, send the answer to the channel, and use the nick
            # as addressing in the message itself:
            d.addCallback(self._sendMessage, channel, nick)

#     def action(self, user, channel, message):
#         log.msg("Performed {} for {}.".format(message, user))

    def _sendMessage(self, msg, target, nick=None):
        if nick:
            msg = "{}, {}".format(nick, msg)
        self.msg(target, msg)

    def _showError(self, failure):
        return failure.getErrorMessage()

    def command_ping(self, rest):
        return "Pong."

    def command_saylater(self, rest):
        when, sep, msg = rest.partition(" ")
        when = int(when)
        d = defer.Deferred()
        # A small example of how to defer the reply from a command. callLater
        # will callback the Deferred with the reply after so many seconds.
        reactor.callLater(when, d.callback, msg)
        # Returning the Deferred here means that it'll be returned from
        # maybeDeferred in privmsg.
        return d


class Factory(protocol.ReconnectingClientFactory):

    def __init__(self, nickname, channels):
        self.nickname = nickname
        self.channels = [i if i.startswith("#") else "#" + i\
                         for i in channels.split(",")]

    def buildProtocol(self, addr):
        p = Protocol(self.nickname)
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()


def main(reactor):

    if not args["--quiet"]:
        log.startLogging(sys.stdout)

    logfile = DailyLogFile.fromFullPath(args["--output"])
    log.addObserver(log.FileLogObserver(logfile).emit)

    # Set the server and port.
    endpoint = endpoints.clientFromString(
        reactor, "tcp:{}:{}".format(args["--server"], args["--port"]))

    # Create the client/protocol factory.
    factory = Factory(args["--nick"], args["--channel"])

    # Finally, return the protocol so we can start.
    d = endpoint.connect(factory)
    d.addCallback(lambda protocol: protocol.deferred)

    return d


if __name__ == "__main__":
    args = docopt(__doc__, version="0.1")
    task.react(main)
