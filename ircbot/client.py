from twisted.internet import defer, protocol, reactor, ssl, threads
from twisted.words.protocols import irc
from twisted.python import rebuild
from types import FunctionType
from reporting import ChatLogger

import sys
import time
import logging
import string
import textwrap

log = logging.getLogger("client")


class CoreCommands(object):

    def command_rehash(self, user, channel, args):
        """Reload modules and optionally the configuration file. Usage: rehash [conf]"""

        if self.factory.is_admin(user):
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
    def command_channels(self, user, channel, args):
        """Usage: channels <network> - List channels the bot is on"""
        if not args:
            self.say(channel, "Please specify a network: %s" % ", ".join(self.factory.clients.keys()))
            return

        self.say(channel, "I am on %s" % self.factory.network.channels)

    def command_help(self, user, channel, cmnd):
        """Get help on all commands or a specific one. Usage: help [<command>]"""

        commands = []
        for module, env in self.factory.ns.items():
            myglobals, mylocals = env
            commands += [(c.replace("command_", ""), ref) for c, ref in mylocals.items() if c.startswith("command_%s" % cmnd)]
        # Help for a specific command
        if len(cmnd):
            for cname, ref in commands:
                if cname == cmnd:
                    helptext = ref.__doc__.split("\n", 1)[0]
                    self.say(channel, "Help for %s: %s" % (cmnd, helptext))
                    return
        # Generic help
        else:
            commandlist = ", ".join([c for c, ref in commands])
            self.say(channel, "Available commands: %s" % commandlist)

    def command_logs(self, rest):
        print rest
        if rest == "off" and self.logs_enabled:
            self.logger.close_logs()
            self.logs_enabled = False
            return "logs are now disabled."
        elif rest == "on" and not self.logs_enabled:
            self.logger.open_logs()
            self.logs_enabled = True
            return "logs are now enabled."

        else:
            if self.logs_enabled:
                return "logs are enabled. Use !logs off to disable logging."
            else:
                return "logs are disabled. Use !logs on to enable logging."

    def command_ping(self, user, channel, args):
        return self.say(channel, "{}, Pong".format(self.factory.get_nick(user)))

    def command_timer(self, user, channel, args):
        when, sep, msg = args.partition(" ")
        when = int(when)
        d = defer.Deferred()
        # A small example of how to defer the reply from a command. callLater
        # will callback the Deferred with the reply after so many seconds.
        r = reactor.callLater(when, d.callback, msg)
        # Returning the Deferred here means that it'll be returned from
        # maybeDeferred in privmsg.
#         return r
        return self.say(channel, "{}, {}".format(self.factory.get_nick(user), d))

class Client(irc.IRCClient, CoreCommands):

    def __init__(self, factory):
        self.factory = factory
        self.nickname = self.identity["nickname"]
        self.realname = self.identity["realname"]
        self.username = self.identity["username"]
        self.wrap = textwrap.TextWrapper(width=400, break_long_words=True)
        self.logs_enabled = True
        self.loglevel = 0
        self.lead = "."
        log.info("Bot initialized")

    def __repr__(self):
        return "demibot(%r, %r)" % (self.nickname,
                                    self.factory.network["server"])

    # Core
    def printResult(self, msg, info):
        # Don't print results if there is nothing to say (usually non-operation on module)
        log.debug("Result %s %s" % (msg, info))

    def printError(self, msg, info):
        log.error("ERROR %s %s" % (msg, info))

    def irc_ERR_NICKNAMEINUSE(self, prefix, params):
        self.identity["nickname"] += "_"

    def _command(self, user, channel, cmnd):
        # Split arguments from the command part
        try:
            cmnd, args = cmnd.split(" ", 1)
        except ValueError:
            args = ""

        # core commands
        method = getattr(self, "command_%s" % cmnd, None)
        if method is not None:
            log.info("internal command %s called by %s (%s) on %s" % (cmnd, user, self.factory.is_admin(user), channel))
            method(user, channel, args)
            return

        # module commands
        for module, env in self.factory.ns.items():
            myglobals, mylocals = env
            # find all matching command functions
            commands = [(c, ref) for c, ref in mylocals.items() if c == "command_%s" % cmnd]

            for cname, command in commands:
                log.info("module command %s called by %s (%s) on %s" % (cname, user, self.factory.is_admin(user), channel))
                # Defer commands to threads
                d = threads.deferToThread(command, self, user, channel, self.factory.to_utf8(args.strip()))
                d.addCallback(self.printResult, "command %s completed" % cname)
                d.addErrback(self.printError, "command %s error" % cname)

    def say(self, channel, message, length=None):
        "Override default say to make replying to private messages easier"

        # Encode channel
        # (for cases where channel is specified in code instead of "answering")
        channel = self.factory.to_utf8(channel)
        # Encode all outgoing messages to UTF-8
        message = self.factory.to_utf8(message)

        # Change nick!user@host -> nick, since all servers don't support full
        # hostmask messaging
        if "!" and "@" in channel:
            channel = self.factory.get_nick(channel)

        # wrap long text into suitable fragments
        msg = self.wrap.wrap(message)
        cont = False

        for m in msg:
            if cont:
                m = "..." + m
            self.msg(channel, m, length)
            cont = True

        return ('client.say', channel, message)

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
            self.logger.close_logs()

    def signedOn(self):
        "Called when the bot has successfully signed on to server"

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
        "Called when the bot joins a channel"
        chatlog = "{}-{}.log".format(channel, self.server)
        self.logger = ChatLogger(open(chatlog, "a"))


    def privmsg(self, user, channel, msg):
        "Called when the bot receives a message"

        chatlog = "{}-{}.log".format(channel, self.server)
        channel = channel.lower()
        lmsg = msg.lower()
        lnick = self.nickname.lower()
        nickl = len(lnick)

        if channel == lnick:
            # Turn private queries into a format we can understand
            if not msg.startswith(self.lead):
                msg = self.lead + msg
            elif lmsg.startswith(lnick):
                msg = self.lead + msg[nickl:].lstrip()
            elif lmsg.startswith(lnick) and len(lmsg) > nickl and\
                                            lmsg[nickl] in string.punctuation:
                msg = self.lead + msg[nickl + 1:].lstrip()
        else:
            # Turn 'nick:' prefixes into self.lead prefixes
            if lmsg.startswith(lnick) and len(lmsg) > nickl and\
                                            lmsg[nickl] in string.punctuation:
                msg = self.lead + msg[len(self.nickname) + 1:].lstrip()
        reply = (channel == lnick) and user or channel

        if msg.startswith(self.lead):
            cmnd = msg[len(self.lead):]
            self._command(user, reply, cmnd)

        # Run privmsg handlers
        self._runhandler("privmsg", user, reply, self.factory.to_utf8(msg))

    def _runhandler(self, handler, *args, **kwargs):

        handler = "handle_%s" % handler
        # module commands
        for module, env in self.factory.ns.items():
            myglobals, mylocals = env
            # find all matching command functions
            handlers = [(h, ref) for h, ref in mylocals.items() if h == handler and type(ref) == FunctionType]

            for hname, func in handlers:
                # defer each handler to a separate thread, assign callbacks to see when they end
                d = threads.deferToThread(func, self, *args, **kwargs)
                d.addCallback(self.printResult, "handler %s completed" % hname)
                d.addErrback(self.printError, "handler %s error" % hname)

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        old_nick = prefix.split("!")[0]
        new_nick = params[0]
        if self.logs_enabled:
            self.logger.log("{} is now known as {}".format(old_nick, new_nick))

    def noticed(self, user, channel, message):
        """I received a notice"""
        self._runhandler("noticed", user, channel, self.factory.to_utf8(message))

    def action(self, user, channel, data):
        """An action"""
        self._runhandler("action", user, channel, self.factory.to_utf8(data))
