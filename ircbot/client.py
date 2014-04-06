from twisted.internet import defer, protocol, reactor, ssl
from twisted.words.protocols import irc
from twisted.python import log
import sys
import time

import plugins  # Import commands and plugins.


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


class Bot(irc.IRCClient):

    def __init__(self):
        self.logs_enabled = True
        self.loglevel = 0
        self.lead = "."

    @property
    def nickname(self):
        return self.factory.identity["nickname"]

    @property
    def realname(self):
        return self.factory.identity["realname"]

    @property
    def username(self):
        return self.factory.identity["username"]

    def irc_ERR_NICKNAMEINUSE(self, prefix, params):
        self.factory.identity["nickname"] += "_"

    def _command(self, user, channel, cmnd):
        # Split arguments from the command part
        try:
            cmnd, args = cmnd.split(" ", 1)
        except ValueError:
            args = ""

        # core commands
        method = getattr(self, "command_%s" % cmnd, None)
        if method is not None:
            log.info("internal command %s called by %s (%s) on %s" % (cmnd, user, self.factory.isAdmin(user), channel))
            method(user, channel, args)
            return

        # module commands
        for module, env in self.factory.ns.items():
            myglobals, mylocals = env
            # find all matching command functions
            commands = [(c, ref) for c, ref in mylocals.items() if c == "command_%s" % cmnd]

            for cname, command in commands:
                log.info("module command %s called by %s (%s) on %s" % (cname, user, self.factory.isAdmin(user), channel))
                # Defer commands to threads
                d = threads.deferToThread(command, self, user, channel, self.factory.to_unicode(args.strip()))
                d.addCallback(self.printResult, "command %s completed" % cname)
                d.addErrback(self.printError, "command %s error" % cname)

    def _sendmsg(self, msg, target, nick=None):
        if nick:
            msg = "{}, {}".format(nick, msg)
        self.msg(target, msg)

    def _showError(self, failure):
        return failure.getErrorMessage()

    def connectionMade(self):
        "Called when a connection to the server has been established"
        irc.IRCClient.connectionMade(self)
        now = time.asctime(time.localtime(time.time()))
        self.logger = ChatLogger(open(self.factory.logfile, "a"))
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

        network = self.factory.network

        if network["identity"]["nickserv_pw"]:
            self.msg("NickServ", "IDENTIFY {}"
                     .format(network["identity"]["nickserv_pw"]))

        for channel in network["channels"]:
            self.join(channel)
            if self.logs_enabled:
                self.logger.log("Joined {} on {}"
                                .format(channel, network["server"]))

    def joined(self, channel):
        "Called when the bot joins the channel."
        pass

    def privmsg(self, user, channel, msg):
        "Called when the bot sees a message (both in the channel or per /msg)."
        nick, _, host = user.partition("!")
        msg = msg.strip()

        # If the message is not a command, log it and do nothing else.
        if not msg.startswith(self.lead):
            if self.logs_enabled:
                self.logger.log("<{}> {}".format(nick, msg))
            return

        # If the message is a command, we handle the logic here.
        command, sep, rest = msg.lstrip(self.lead).partition(" ")
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

        # Check to see if they"re sending me a private msg
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

    def command_rehash(self, user, channel, args):
        """Reload modules and optionally the configuration file. Usage: rehash [conf]"""

        if self.factory.isAdmin(user):
            try:
                # rebuild core & update
                log.info("rebuilding %r" % self)
                rebuild.updateInstance(self)

                # reload config file
                if args == 'conf':
                    self.factory.reload_config()
                    self.say(channel, 'Configuration reloaded.')

                # unload removed modules
                self.factory._unload_removed_modules()
                # reload modules
                self.factory._loadmodules()
            except Exception, e:
                self.say(channel, "Rehash error: %s" % e)
                log.error("Rehash error: %s" % e)
            else:
                self.say(channel, "Rehash OK")
                log.info("Rehash OK")

    def command_logs(self, rest):
        print rest
        if rest == "off" and self.logs_enabled:
            self.logger.close()
            self.logs_enabled = False
            return "logs are now disabled."
        elif rest == "on" and not self.logs_enabled:
            self.logger = ChatLogger(open(self.factory.logfile, "a"))
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

    protocol = Bot

    def __init__(self, network_name, network, logfile="demibot.log"):
        self.network_name = network_name
        self.network = network
        self.logfile = logfile
        self.identity = self.network["identity"]

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        print("Client connection lost")
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print("Client connection failed")
        reactor.stop()
