import logging
import string
import textwrap
from types import FunctionType

from twisted.internet import threads
from twisted.python import rebuild
from twisted.words.protocols import irc

from reporting import ChatLogger


log = logging.getLogger("client")


class CoreCommands(object):

    def command_rehash(self, user, channel, args):
        "Rehashes all available modules to reflect any changes."

        if self.factory.is_superadmin(user):
            try:
                log.info("Rebuilding {}".format(self))
                rebuild.updateInstance(self)
                self.factory._unload_removed_modules()
                self.factory._loadmodules()
            except Exception, e:
                log.error("Rehash error: {}".format(e))
                return self.say(channel, "Rehash error: {}".format(e))
            else:
                log.info("Rehash OK")
                return self.say(channel, "Rehash OK")
        else:
            return self.say(channel, "Requires admin rights")

    def command_join(self, user, channel, args):
        "Usage: join <channel>... (Comma separated, hash not required)"

        if not self.factory.is_admin(user):
            return

        channels = [i if i.startswith("#") else "#" + i\
                    for i in args.split(",")]
        network = self.factory.network

        for c in channels:
            log.debug("Attempting to join channel {}.".format(c))
            if c in network["channels"]:
                self.say(channel, "I am already in {}".format(c))
                log.debug("Already on channel {}".format(c))
                log.debug("Channels I'm on this network: {}"
                          .format(", ".join(network["channels"])))
            else:
                self.say(channel, "Joining {}.".format(c))
                self.join(c)

    def command_leave(self, user, channel, args):
        "Usage: leave <channel>"

        if not self.factory.is_admin(user):
            return

        network = self.factory.network

        # No arguments, so we leave the current channel.
        if not args:
            self.part(channel)
            return

        # We have input, so split it into channels.
        channels = [i if i.startswith("#") else "#" + i\
                    for i in args.split(",")]

        for c in channels:
            if c in network["channels"]:
                self.part(c)
            else:
                self.say(channel, "I am not in {}".format(c))
                log.debug("Attempted to leave a channel i'm not in: {}"
                          .format(c))

            log.debug("Channels I'm in: {}"
                      .format(", ".join(network["channels"])))

    def command_channels(self, user, channel, args):
        "List channels the bot is on. No arguments."

        return self.say(channel, "I am on {}"
                        .format(", ".join(self.factory.network["channels"])))

    def command_help(self, user, channel, cmnd):
        "Get help on all commands or a specific one. Usage: help [<command>]"

        commands = []
        for module, env in self.factory.ns.items():
            myglobals, mylocals = env
            commands += [(c.replace("command_", ""), ref) for c, ref in\
                         mylocals.items() if c.startswith("command_%s" % cmnd)]
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
            self.say(channel, "Available commands: {}".format(commandlist))

    def command_logs(self, user, channel, args):
        if args == "off" and self.factory.logs_enabled:
            self.chatlogger.close_logs()
            self.factory.logs_enabled = False
            log.debug("Chatlogs enabled")
            return self.say(channel, "Chatlogs are now disabled.")
        elif args == "on" and not self.factory.logs_enabled:
            self.chatlogger.open_logs(self.factory.network["channels"])
            self.factory.logs_enabled = True
            log.debug("Chatlogs disabled")
            return self.say(channel, "Chatlogs are now enabled.")
        else:
            if self.factory.logs_enabled:
                return self.say(channel,
                    "Logs are enabled. Use !logs off to disable logging.")
            else:
                return self.say(channel,
                    "Logs are disabled. Use !logs on to enable logging.")

    def command_loglevel(self, user, channel, args):
        return self.say(channel, "Log level is {}."
                        .format(log.getEffectiveLevel()))

    def command_ping(self, user, channel, args):
        return self.say(channel,
                        "{}, Pong.".format(self.factory.get_nick(user)))


class Client(irc.IRCClient, CoreCommands):

    def __init__(self, factory):
        self.factory = factory
        self.nickname = self.factory.network["identity"]["nickname"]
        self.realname = self.factory.network["identity"]["realname"]
        self.username = self.factory.network["identity"]["username"]
        self.wrap = textwrap.TextWrapper(width=400, break_long_words=True)
        self.lead = "."
        log.info("Bot initialized")

    def __repr__(self):
        return "demibot({}, {})".format(self.nickname,
                                        self.factory.network["server"])

    def printResult(self, msg, info):
        # Don't print results if there is nothing to say (usually non-operation
        # on module)
        log.debug("Result {} {}".format(msg, info))

    def printError(self, msg, info):
        log.error("ERROR {} {}".format(msg, info))

    def irc_ERR_NICKNAMEINUSE(self, prefix, params):
        self.factory.network["identity"]["nickname"] += "_"

    def _command(self, user, channel, cmnd):
        # Split arguments from the command part
        try:
            cmnd, args = cmnd.split(" ", 1)
        except ValueError:
            args = ""

        # core commands
        method = getattr(self, "command_{}".format(cmnd), None)
        if method is not None:
            log.info("Internal command {} called by {} ({}) on {}"
                     .format(cmnd, user, self.factory.is_admin(user), channel))
            method(user, channel, args)
            return

        # module commands
        for module, env in self.factory.ns.items():
            myglobals, mylocals = env
            # find all matching command functions
            commands = [(c, ref) for c, ref in mylocals.items() if\
                        c == "command_{}".format(cmnd)]

            for cname, command in commands:
                log.info("Module command {} called by {} ({}) on {}"
                         .format(cname, user, self.factory.is_admin(user),
                                 channel))
                # Defer commands to threads
                d = threads.deferToThread(command, self, user, channel,
                                          self.factory.to_utf8(args.strip()))
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
        if self.factory.logs_enabled:
            self.chatlogger = ChatLogger(self.factory.network_name)
            self.chatlogger.open_logs(self.factory.network["channels"])

    def connectionLost(self, reason):
        "Called when a connection to the server has been lost"
        irc.IRCClient.connectionLost(self, reason)
        if self.factory.logs_enabled:
            self.chatlogger.close_logs()

    def signedOn(self):
        "Called when the bot has successfully signed on to server"

        network = self.factory.network

        if network["identity"]["nickserv_pw"]:
            self.msg("NickServ", "IDENTIFY {}"
                     .format(network["identity"]["nickserv_pw"]))

        for channel in network["channels"]:
            self.join(channel)

    def joined(self, channel):
        "Called when the bot joins a channel"
        log.info("Joined {} on {}".format(channel,
                                          self.factory.network["server"]))

        # Adds the channel to the relevant sets/dicts.
        self.factory.network["channels"].add(channel)
        if self.factory.logs_enabled:
            self.chatlogger.add_channel(channel)

    def left(self, channel):
        "Called when the bot has left a channel"
        log.info("Left {} on {}".format(channel,
                                          self.factory.network["server"]))

        # Remove the channel from the channel set.
        self.factory.network["channels"].discard(channel)
        if self.factory.logs_enabled:
            self.chatlogger.del_channel(channel)

    def privmsg(self, user, channel, msg):
        "Called when the bot receives a message"

        channel = channel.lower()
        lmsg = msg.lower()
        lnick = self.nickname.lower()
        nickl = len(lnick)

        # Log the message to a chatfile but ignore private messages.
        if self.factory.logs_enabled and channel != lnick:
            self.chatlogger.log("<{}> {}".format(self.factory.get_nick(user),
                                                 msg), channel)
            # If there is a url in the message, log it to logs/url-server.log.
            if "http://" or "www." in msg:
                splitmsg = msg.lower().split()
                for i in splitmsg:
                    if i.startswith("www") or i.startswith("http://"):
                        self.chatlogger.log_url(i)

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

        handler = "handle_{}".format(handler)
        # module commands
        for module, env in self.factory.ns.items():
            myglobals, mylocals = env
            # find all matching command functions
            handlers = [(h, ref) for h, ref in mylocals.items()\
                        if h == handler and type(ref) == FunctionType]

            for hname, func in handlers:
                # Defer each handler to a separate thread, assign callbacks to
                # see when they end.
                d = threads.deferToThread(func, self, *args, **kwargs)
                d.addCallback(self.printResult, "handler %s completed" % hname)
                d.addErrback(self.printError, "handler %s error" % hname)

    def noticed(self, user, channel, message):
        "I received a notice"
        self._runhandler("noticed", user, channel,
                         self.factory.to_utf8(message))

    def action(self, user, channel, data):
        "An action"
        self._runhandler("action", user, channel, self.factory.to_utf8(data))
