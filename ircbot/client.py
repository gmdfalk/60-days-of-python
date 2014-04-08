import logging
import string
import textwrap
from types import FunctionType

from twisted.internet import threads
from twisted.words.protocols import irc

from reporting import ChatLogger


log = logging.getLogger("client")


class Client(irc.IRCClient):

    def __init__(self, factory):
        self.factory = factory
        self.nickname = self.factory.network["identity"]["nickname"]
        self.realname = self.factory.network["identity"]["realname"]
        self.username = self.factory.network["identity"]["username"]
        self.sourceURL = self.factory.URL  # CTCP source queries to the github.
        self.lineRate = 0.5  # print at most 0.5 lines per second.
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
                     .format(cmnd, user, self.factory.permissions(user),
                             channel))
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
                         .format(cname, user, self.factory.permissions(user),
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
        try:
            msg = self.wrap.wrap(message)
        except AttributeError as e:
            log.debug("Could not wrap {}: {}".format(message, e))
            msg = ""

        cont = False

        for m in msg:
            if cont:
                m = "..." + m
            self.msg(channel, m, length)
            cont = True

        return ("client.say", channel, message)

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

        # Log messages to a chatfile except private ones.
        if self.factory.logs_enabled and channel != lnick:
            self.chatlogger.log("<{}> {}".format(self.factory.get_nick(user),
                                                 msg), channel)

        # URL Handling.
        if "www" in msg or "http" in msg:
            url = self.factory.get_url(msg)
            if url:
                log.debug("URL detected: {}".format(url))
                if self.factory.titles_enabled:
                    self.say(channel, self.factory.get_title(url))
                if self.factory.logs_enabled:
                    self.chatlogger.log_url("<{}> {}".format(
                                            self.factory.get_nick(user), msg),
                                            channel)

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
