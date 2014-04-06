# coding: utf-8
from twisted.internet import defer, protocol, reactor, ssl, threads
from twisted.words.protocols import irc
from twisted.python import log, rebuild
from types import FunctionType

import os
import sys
import time
import logging
import fnmatch
import string
import textwrap


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

    def __init__(self, factory):
        self.factory = factory
        self.logs_enabled = True
        self.loglevel = 0
        self.lead = "."
        self.tw = textwrap.TextWrapper(width=400, break_long_words=True)
        self.nickname = self.factory.identity["nickname"]
        self.realname = self.factory.identity["realname"]
        self.username = self.factory.identity["username"]
#         log.info("Bot initialized")

    def __repr__(self):
        return "demibot(%r, %r)" % (self.nickname,
                                    self.factory.network["server"])

    # Core
    def printResult(self, msg, info):
        # Don't print results if there is nothing to say (usually non-operation on module)
#         if msg:
#             log.debug("Result %s %s" % (msg, info))
        pass

    def printError(self, msg, info):
#         log.error("ERROR %s %s" % (msg, info))
        pass

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
#             log.info("internal command %s called by %s (%s) on %s" % (cmnd, user, self.factory.isAdmin(user), channel))
            method(user, channel, args)
            return

        # module commands
        for module, env in self.factory.ns.items():
            myglobals, mylocals = env
            # find all matching command functions
            commands = [(c, ref) for c, ref in mylocals.items() if c == "command_%s" % cmnd]

            for cname, command in commands:
#                 log.info("module command %s called by %s (%s) on %s" % (cname, user, self.factory.isAdmin(user), channel))
                # Defer commands to threads
                d = threads.deferToThread(command, self, user, channel, self.factory.to_utf8(args.strip()))
                d.addCallback(self.printResult, "command %s completed" % cname)
                d.addErrback(self.printError, "command %s error" % cname)

    def say(self, channel, message, length=None):
        """Override default say to make replying to private messages easier"""

        # Encode channel
        # (for cases where channel is specified in code instead of "answering")
        channel = self.factory.to_utf8(channel)
        # Encode all outgoing messages to UTF-8
        message = self.factory.to_utf8(message)

        # Change nick!user@host -> nick, since all servers don't support full hostmask messaging
        if "!" and "@" in channel:
            channel = self.factory.getNick(channel)

        # wrap long text into suitable fragments
        msg = self.tw.wrap(message)
        cont = False

        for m in msg:
            if cont:
                m = "..." + m
            self.msg(channel, m, length)
            cont = True

        return ('botcore.say', channel, message)

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
        "This will get called when the bot receives a message"

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
            elif lmsg.startswith(lnick) and len(lmsg) > nickl and lmsg[nickl] in string.punctuation:
                msg = self.lead + msg[nickl + 1:].lstrip()
        else:
            # Turn 'nick:' prefixes into self.lead prefixes
            if lmsg.startswith(lnick) and len(lmsg) > nickl and lmsg[nickl] in string.punctuation:
                msg = self.lead + msg[len(self.nickname) + 1:].lstrip()
        reply = (channel == lnick) and user or channel

        if msg.startswith(self.lead):
            cmnd = msg[len(self.lead):]
            self._command(user, reply, cmnd)

        # Run privmsg handlers
        self._runhandler("privmsg", user, reply, self.factory.to_utf8(msg))

    def _runhandler(self, handler, *args, **kwargs):
        """Run a handler for an event"""
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

    def command_ping(self, user, channel, args):
        return self.say(channel, "{}, Pong".format(self.factory.getNick(user)))

    def command_timer(self, user, channel, args):
        when, sep, msg = args.partition(" ")
        when = int(when)
        d = defer.Deferred()
        # A small example of how to defer the reply from a command. callLater
        # will callback the Deferred with the reply after so many seconds.
        reactor.callLater(when, d.callback, msg)
        # Returning the Deferred here means that it'll be returned from
        # maybeDeferred in privmsg.
        return self.say(channel, "{}, {}".format(self.factory.getNick(user), d))

    def command_rehash(self, user, channel, args):
        """Reload modules and optionally the configuration file. Usage: rehash [conf]"""

        if self.factory.isAdmin(user):
            try:
                # rebuild core & update
#                 log.info("rebuilding %r" % self)
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
#                 log.error("Rehash error: %s" % e)
            else:
                self.say(channel, "Rehash OK")
#                 log.info("Rehash OK")

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

#     protocol = Bot
    moduledir = os.path.join(sys.path[0], "modules/")

    def __init__(self, network_name, network, logfile="demibot.log"):
        self.network_name = network_name
        self.network = network
        self.logfile = logfile
        self.identity = self.network["identity"]
        self.ns = {}


    def startFactory(self):
        self._loadmodules()
#         log.info("Factory started")

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
#         log.warn("Client connection lost")
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
#         log.warn("Client connection failed")
        reactor.stop()

    def buildProtocol(self, address):
        # we are connecting to a server, don't know which yet
#         log.info("Building protocol for %s", address)
        p = Bot(self)
        return p

    def _finalize_modules(self):
        """Call all module finalizers"""
        for module in self._findmodules():
            # if rehashing (module already in namespace), finalize the old instance first
            if module in self.ns:
                if 'finalize' in self.ns[module][0]:
#                     log.info("finalize - %s" % module)
                    self.ns[module][0]['finalize']()

    def _loadmodules(self):
        """Load all modules"""
        self._finalize_modules()
        for module in self._findmodules():
            env = self._getGlobals()
#             log.info("load module - %s" % module)
            # Load new version of the module
            execfile(os.path.join(self.moduledir, module), env, env)
            # Initialize module
            if 'init' in env:
#                 log.info("initialize module - %s" % module)
                env['init'](self)
            # Add to namespace so we can find it later
            self.ns[module] = (env, env)

    def _unload_removed_modules(self):
        """Unload modules removed from modules -directory"""
        # find all modules in namespace, which aren't present in modules -directory
        removed_modules = [m for m in self.ns if not m in self._findmodules()]

        for m in removed_modules:
            # finalize module before deleting it
            # TODO: use general _finalize_modules instead of copy-paste
            if 'finalize' in self.ns[m][0]:
#                 log.info("finalize - %s" % m)
                self.ns[m][0]['finalize']()
            del self.ns[m]
#             log.info('removed module - %s' % m)

    def _findmodules(self):
        """Find all modules"""
        modules = [m for m in os.listdir(self.moduledir) if m.startswith("module_") and m.endswith(".py")]
        return modules

    def _getGlobals(self):
        """Global methods for modules"""
        g = {}

        g['getNick'] = self.getNick
        g['getIdent'] = self.getIdent
        g['getHost'] = self.getHost
        g['isAdmin'] = self.isAdmin
        g['to_utf8'] = self.to_utf8
        g['to_unicode'] = self.to_unicode
        return g

    def getNick(self, user):
        "Parses nick from nick!user@host"
        return user.split('!', 1)[0]

    def getIdent(self, user):
        "Parses ident from nick!user@host"
        return user.split('!', 1)[1].split('@')[0]

    def getHost(self, user):
        "Parses host from nick!user@host"
        return user.split('@', 1)[1]

    def isAdmin(self, user):
        "Check if an user has admin privileges."
        for pattern in self.config['admins']:
            if fnmatch.fnmatch(user, pattern):
                return True
        return False

    def to_utf8(self, _string):
        "Convert string to UTF-8 if it is unicode"
        if isinstance(_string, unicode):
            _string = _string.encode("UTF-8")
        return _string

    def to_unicode(self, _string):
        "Convert string to UTF-8 if it is unicode"
        if not isinstance(_string, unicode):
            try:
                _string = unicode(_string)
            except:
                try:
                    _string = _string.decode('utf-8')
                except:
                    _string = _string.decode('iso-8859-1')
        return _string


def init_logging(config):
    logger = logging.getLogger()

    if config.get('debug', False):
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)


    FORMAT = "%(asctime)-15s %(levelname)-8s %(name)-11s %(message)s"
    formatter = logging.Formatter(FORMAT)
    # Append file name + number if debug is enabled
    if config.get('debug', False):
        FORMAT = "%s %s" % (FORMAT, " (%(filename)s:%(lineno)d)")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
