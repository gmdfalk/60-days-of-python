#!/usr/bin/env python2
"""IRCBot

Usage:
    ircbot.py [-h] [-s <server>] [-p <port>] [--password=<pass>] [-c <chans>]
              [-n <nick>] [-o <file>]  [--max-tries N] [-v N] [-q]

Options:
    -s, --server=<server>    DNS address [default: irc.freenode.net]
    -p, --port=<port>        Port number of the IRC server [default: 6667]
    -pw, --password=<pass>   Server password, if required
    -c, --channels=<chans>   Channels, comma separated [default: z1,z2,z3]
    -n, --nick=<nick>        Nickname of the bot [default: maxbot]
    -o, --output=<file>      Logging file [default: test.log]
    --max-tries N            Limit retries on network errors [default: 4]
    -h, --help               Show this help msg and exit
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
# Seen (track last msg by user x)
# Conduct a poll.
# Evaluate python/bash
# Dictionary, wiki
# Search channel log.
# msg system (leaving a notification)


# twisted imports
from twisted.internet import defer, protocol, reactor
from twisted.words.protocols import irc
from twisted.python import log
from docopt import docopt
import sys
import time
import plugins  # Import commands and plugins.


class ChatLogger(object):
    """
    An independent logger class (because separation of application
    and protocol logic is a good thing).
    """
    def __init__(self, file):
        self.file = file

    def log(self, msg):
        """Write a log line to the file with timestamp."""
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        self.file.write("{} {}\n".format(timestamp, msg))
        self.file.flush()

    def close(self):
        self.file.close()


class Protocol(irc.IRCClient):
    """A logging IRC bot."""

    def __init__(self, factory, nickname):
        self.factory = factory
        self.nickname = nickname
        self.logs_enabled = True

    def connectionMade(self):
        "Called when a connection to the server has been established"
        irc.IRCClient.connectionMade(self)
        now = time.asctime(time.localtime(time.time()))
        self.logger = ChatLogger(open(self.factory.filename, "a"))
        self.logger.log("Connected at {}".format(now))

    def connectionLost(self, reason):
        "Called when a connection to the server has been lost"
        irc.IRCClient.connectionLost(self, reason)
        now = time.asctime(time.localtime(time.time()))
        if self.logs_enabled:
            self.logger.log("Disconnected at {}".format(now))
            self.logger.close()

    def signedOn(self):
        "Called when the bot has successfully signed on to server."
        for channel in self.factory.channels:
                    self.join(channel)

    def joined(self, channel):
        "Called when the bot joins the channel."
        if self.logs_enabled:
            self.logger.log("Joined {}".format(channel))

    def privmsg(self, user, channel, msg):
        "Called when the bot sees a message (both in the channel or per /msg)."
        nick, _, host = user.partition("!")
        msg = msg.strip()

        # If the message is not a command, log it and do nothing else.
        if not msg.startswith("!"):
            if self.logs_enabled:
                self.logger.log("<{}> {}".format(nick, msg))
            return

        # If the message is a command, we handle the logic here.
        command, sep, rest = msg.lstrip("!").partition(" ")
        # Get the function corresponding to the command given.
        func = getattr(self, "command_" + command, None)
        # Or, if there was no function, ignore the msg.
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
        # error into a terse msg first:
        d.addErrback(self._showError)
        # Whatever is returned is sent back as a reply:
        if channel == self.nickname:
            # When channel == self.nickname, the msg was sent to the bot
            # directly and not to a channel. So we will answer directly too:
            d.addCallback(self._sendmsg, nick)
        else:
            # Otherwise, send the answer to the channel, and use the nick
            # as addressing in the msg itself:
            d.addCallback(self._sendmsg, channel, nick)

        # Check to see if they're sending me a private msg
        if channel == self.nickname:
            message = "It isn't nice to whisper!  Play nice with the group."
            self.msg(nick, message)
            return

        # Otherwise check to see if it is a msg directed at me
        if msg.startswith(self.nickname + ":"):
            message = "{}: I am not your friend".format(nick)
            self.msg(channel, message)
            if self.logs_enabled:
                self.logger.log("<{}> {}".format(self.nickname, message))

    def _sendmsg(self, msg, target, nick=None):
        if nick:
            msg = "{}, {}".format(nick, msg)
        self.msg(target, msg)

    def _showError(self, failure):
        return failure.getErrorMessage()

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        user = user.split("!", 1)[0]
        if self.logs_enabled:
            self.logger.log("* {} {}".format(user, msg))

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        old_nick = prefix.split("!")[0]
        new_nick = params[0]
        if self.logs_enabled:
            self.logger.log("{} is now known as {}".format(old_nick, new_nick))

    def command_ping(self, rest):
        return "Pong."

    def command_timer(self, rest):
        when, sep, msg = rest.partition(" ")
        when = int(when)
        d = defer.Deferred()
        # A small example of how to defer the reply from a command. callLater
        # will callback the Deferred with the reply after so many seconds.
        reactor.callLater(when, d.callback, msg)
        # Returning the Deferred here means that it'll be returned from
        # maybeDeferred in privmsg.
        return d

    def command_logs(self, rest):
        print rest
        if rest == "off" and self.logs_enabled:
            self.logger.close()
            self.logs_enabled = False
            return "logs are now disabled."
        elif rest == "on" and not self.logs_enabled:
            self.logger = ChatLogger(open(self.factory.filename, "a"))
            self.logs_enabled = True
            return "logs are now enabled."

        else:
            if self.logs_enabled:
                return "logs are enabled. Use !logs off to disable logging."
            else:
                return "logs are disabled. Use !logs on to enable logging."


class Factory(protocol.ClientFactory):
    """A factory for LogBots.

    A new protocol instance will be created each time we connect to the server.
    """

    def __init__(self, channels, nickname, filename):
        self.channels = [i if i.startswith("#") else "#" + i\
                         for i in channels.split(",")]
        self.nickname = nickname
        self.filename = filename


    def buildProtocol(self, addr):
        p = Protocol(self, self.nickname)
        return p

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()


def main():
    args = docopt(__doc__, version="0.1")

    if not args["--quiet"]:
        log.startLogging(sys.stdout)

    # create factory protocol and application, channel, filename
    factory = Factory(args["--channels"], args["--nick"], args["--output"])

    # connect factory to this host and port
    reactor.connectTCP(args["--server"], int(args["--port"]), factory)

    # run bot
    reactor.run()

if __name__ == "__main__":
    main()
