"""Core Commands

    The basic bot commands.

    Sorted by permission:
        * help (0, public)
        * version
        * me
        * join (10, admin)
        * leave
        * settopic
        * channels
        * logs
        * kick
        * quit (20, superadmin)
        * tempban
        * mode
        * setnick
        * admins
        * rehash
        * printvars
"""
# TODO: Return out of mode, tempban, kick if we're not channel OP.

import logging
import re

from twisted.internet import reactor
from twisted.python import rebuild


log = logging.getLogger("core")


def command_admins(bot, user, channel, args):
    "Add, remove or list admins. Usage: admins [(add|del) <nick>,...]"
    if permissions(user) < 20:  # 0 public, 1-9 undefined, 10-19 admin, 20 root
        return bot.say(channel, "{}, insufficient permissions.".format(
                       get_nick(user)))

    superadmins = bot.factory.network["superadmins"]
    admins = superadmins ^ bot.factory.network["admins"]

    str_sadmins = " ".join(superadmins)
    str_admins = " ".join(admins) if admins else 0

    if not args:
        return bot.say(channel, "superadmins: {}, admins: {}"
                       .format(str_sadmins, str_admins))

    args = args.split()
    if len(args) > 2:
        return bot.say(channel, "Too many arguments.")
    elif len(args) == 1:
        return bot.say(channel, "Not enough arguments.")


    mod_admins = None
    if "," in args[1]:
        # Create the list of entities to add/del but ignore superadmins.
        mod_admins = [i for i in args[1].split(",") if i not in superadmins]
    else:
        if args[1] in superadmins:
            return bot.say(channel, "Cannot modify superadmins.")

    # Handle addition and removal of admins.
    if args[0] == "del":
        if mod_admins:
            for i in mod_admins:
                if i in admins:
                    bot.factory.network["admins"].discard(i)
                    bot.say(channel, "Removed {} from admins.".format(i))
                    log.debug("Discarded {} from admins.".format(i))
        else:
            bot.factory.network["admins"].discard(args[1])
            bot.say(channel, "Removed {} from admins.".format(args[1]))
            log.debug("Discarded {} from admins.".format(args[1]))
    elif args[0] == "add":
        if mod_admins:
            for i in mod_admins:
                if i not in admins:
                    bot.factory.network["admins"].add(i)
                    bot.say(channel, "Added {} to admins.".format(i))
                    log.debug("Added {} to admins.".format(i))
        else:
            bot.factory.network["admins"].add(args[1])
            bot.say(channel, "Added {} to admins.".format(args[1]))
            log.debug("Added {} to admins.".format(args[1]))


def command_rehash(bot, user, channel, args):
    "Rehashes all available modules to reflect any changes."

    if permissions(user) < 20:  # 0 public, 1-9 undefined, 10-19 admin, 20 root
        return bot.say(channel, "{}, insufficient permissions.".format(
                       get_nick(user)))

    try:
        log.info("Rebuilding {}".format(bot))
        rebuild.updateInstance(bot)
        bot.factory._unload_removed_modules()
        bot.factory._loadmodules()
    except Exception, e:
        log.error("Rehash error: {}.".format(e))
        return bot.say(channel, "Rehash error: {}.".format(e))
    else:
        log.info("Rehash OK.")
        return bot.say(channel, "Rehash OK.")


def command_quit(bot, user, channel, args):
    "Ends this or optionally all client instances. Usage: quit [all]."

    if permissions(user) < 20:  # 0 public, 1-9 undefined, 10-19 admin, 20 root
        return bot.say(channel, "{}, insufficient permissions.".format(
                       get_nick(user)))

    if args == "all":
        reactor.stop()

    bot.factory.retry_enabled = False
    log.info("Received quit command for {} from {}. Bye."
             .format(bot.factory.network_name, user))
    bot.quit()


def command_kick(bot, user, channel, args, reason=None):
    "Usage: kick <user> [<reason>]"
    if permissions(user) < 10:  # 0 public, 1-9 undefined, 10-19 admin, 20 root
        return bot.say(channel, "{}, insufficient permissions.".format(
                       get_nick(user)))

    args = [i for i in args.partition(" ") if i and i != " "]
    if len(args) > 2:
        return bot.say(channel, "Usage: kick <user> [<reason>]")
    else:
        reason = args[1]
    usr = args[0]

    bot.kick(channel, usr, reason)


def command_mode(bot, user, channel, args):
    "Usage: mode <(+|-)mode> <user> [<channel>]"
    # TODO: "all" argument instead of user.
    if permissions(user) < 20:  # 0 public, 1-9 undefined, 10-19 admin, 20 root
        return bot.say(channel, "{}, insufficient permissions.".format(
                       get_nick(user)))

    args = args.split()
    if len(args) > 3 or len(args) < 2:
        return bot.say(channel, "Usage: mode <(+|-)mode> <user> [<channel>]")
    elif len(args) == 3:
        chan = args[2]
    else:
        chan = channel
    mode, usr = args[0], args[1]

    if len(mode) == 2:
        if "+" in mode:
            operation, finalmode = True, mode.strip("+")
        elif "-" in mode:
            operation, finalmode = False, mode.strip("-")
    else:
        return bot.say(channel, "Mode have this format: +b")

    bot.mode(chan, operation, finalmode, user=usr)


def command_tempban(bot, user, channel, args):
    "Usage: tempban <duration> <user> [<channel>]"
    if permissions(user) < 20:  # 0 public, 1-9 undefined, 10-19 admin, 20 root
        return bot.say(channel, "{}, insufficient permissions.".format(
                       get_nick(user)))

    args = args.split()
    if len(args) > 3 or len(args) < 2:
        return bot.say(channel, "Usage: tempban <duration> <user> [<channel>]")
    elif len(args) == 3:
        chan = args[2]
    else:
        chan = channel
    duration, usr = args[0].lower(), args[1]

    # Accept only valid duration input e.g. 5, 5d, 5h, 5m.
    _valid_duration = re.compile("[0-9]+[mhd]?")
    def valid_duration(d):
        return bool(_valid_duration.search(d))

    if len(duration) > 2 or not valid_duration(duration):
        return bot.say(channel, "Duration can be 5, 5m, 5h, 5d")

    if "m" in duration:
        cut_duration = int(duration.strip("m")) * 60
    elif "h" in duration:
        cut_duration = int(duration.strip("h")) * 3600
    elif "d" in duration:
        cut_duration = int(duration.strip("d")) * 86400
    else:
        cut_duration = int(duration)

    bot.say(chan, "Banning {} for {}.".format(usr, duration))
    log.info("Banning {} for {} on {}.".format(usr, duration, chan))
    bot.mode(chan, True, "b", user=usr)
    reactor.callLater(cut_duration, bot.mode, chan, False, "b", user=usr)


def command_setnick(bot, user, channel, args):
    "Change the bots nickname. Usage: setnick <nick>"
    if permissions(user) < 20:  # 0 public, 1-9 undefined, 10-19 admin, 20 root
        return bot.say(channel, "{}, insufficient permissions.".format(
                       get_nick(user)))

    args = args.split()
    if len(args) > 1:
        return

    bot.factory.network["identity"]["nickname"] = args[0]
    bot.nickname = bot.factory.network["identity"]["nickname"]
    bot.setNick(bot.nickname)
    log.info("Changed nickname to {}".format(args[0]))


def command_setmin(bot, user, channel, args):
    "Change the bots nickname. Usage: setnick <nick>"
    level, nick = permissions(user), get_nick(user)
    if level < 20:  # 0 public, 1-9 undefined, 10-19 admin, 20 root
        return bot.say(channel, "{}, insufficient permissions.".format(nick))

    if len(args.split()) > 1 or not args.isdigit():
        return bot.say(channel, "Minperms: {}".format(bot.factory.minperms))

    minperm = int(args)
    if minperm > level:  # Don't shut yourself out.
        return bot.say(channel, "Your maximum is {}, {}".format(level, nick))
        minperm = 20

    bot.factory.minperms = minperm
    log.info("Minperms set to {}".format(bot.factory.minperms))
    return bot.say(channel, "Minperms set to: {}".format(bot.factory.minperms))


def command_settopic(bot, user, channel, args):
    "Set the channel topic. Usage: settopic <topic>"
    if permissions(user) < 10:  # 0 public, 1-9 undefined, 10-19 admin, 20 root
        return bot.say(channel, "{}, insufficient permissions.".format(
                       get_nick(user)))

    if not args:
        return bot.say(channel, "Usage: settopic <topic>")

    bot.topic(channel, args)
    log.info("Changed {}'s topic to {}".format(channel, args))


def command_join(bot, user, channel, args):
    "Usage: join <channel>,... (Comma separated, hash not required)."

    if permissions(user) < 10:  # 0 public, 1-9 undefined, 10-19 admin, 20 root
        return bot.say(channel, "{}, insufficient permissions.".format(
                       get_nick(user)))

    channels = [i if i.startswith("#") else "#" + i\
                for i in args.split(",")]
    network = bot.factory.network

    for c in channels:
        log.debug("Attempting to join channel {}.".format(c))
        if c in network["channels"]:
            bot.say(channel, "I am already in {}".format(c))
            log.debug("Already on channel {}".format(c))
            log.debug("Channels I'm on this network: {}"
                      .format(", ".join(network["channels"])))
        else:
            bot.say(channel, "Joining {}.".format(c))
            bot.join(c)


def command_leave(bot, user, channel, args):
    "Usage: leave <channel>,... (Comma separated, hash not required)."

    if permissions(user) < 10:  # 0 public, 1-9 undefined, 10-19 admin, 20 root
        return bot.say(channel, "{}, insufficient permissions.".format(
                       get_nick(user)))

    network = bot.factory.network

    # No arguments, so we leave the current channel.
    if not args:
        bot.part(channel)
        return

    # We have input, so split it into channels.
    channels = [i if i.startswith("#") else "#" + i\
                for i in args.split(",")]

    for c in channels:
        if c in network["channels"]:
            if c != channel:
                bot.say(channel, "Leaving {}".format(c))
            bot.part(c)
        else:
            bot.say(channel, "I am not in {}".format(c))
            log.debug("Attempted to leave a channel i'm not in: {}"
                      .format(c))

        log.debug("Channels I'm in: {}"
                  .format(", ".join(network["channels"])))


def command_channels(bot, user, channel, args):
    "List channels the bot is on."
    if permissions(user) < 10:  # 0 public, 1-9 undefined, 10-19 admin, 20 root
        return bot.say(channel, "{}, insufficient permissions.".format(
                       get_nick(user)))

    return bot.say(channel, "I am on {}"
                    .format(",".join(bot.factory.network["channels"])))


def command_help(bot, user, channel, cmnd):
    "Get help on all commands or a specific one. Usage: help [<command>]"
    # TODO: Only print commands that are available to the user.
    commands = []
    for module, env in bot.factory.ns.items():
        myglobals, mylocals = env
        commands += [(c.replace("command_", ""), ref) for c, ref in\
                     mylocals.items() if c.startswith("command_%s" % cmnd)]
    # Help for a specific command
    if len(cmnd):
        for cname, ref in commands:
            if cname == cmnd:
                helptext = ref.__doc__.split("\n", 1)[0]
                bot.say(channel, "Help for %s: %s" % (cmnd, helptext))
                return
    # Generic help
    else:
        commandlist = ", ".join([c for c, ref in commands])
        bot.say(channel, "Available commands: {}".format(commandlist))


def command_logs(bot, user, channel, args):
    "Usage: logs [on|off|level]."
    if bot.factory.mininum_permissions > permissions(user) < 20:
        return bot.say(channel, "{}, insufficient permissions.".format(
                       get_nick(user)))

    if args == "off" and bot.factory.logs_enabled:
        bot.factory.logs_enabled = False
        bot.chatlogger.close_logs()
        log.info("Chatlogs enabled")
        return bot.say(channel, "Chatlogs are now disabled.")
    elif args == "on" and not bot.factory.logs_enabled:
        bot.factory.logs_enabled = True
        bot.chatlogger.open_logs(bot.factory.network["channels"])
        log.info("Chatlogs disabled")
        return bot.say(channel, "Chatlogs are now enabled.")
    elif args == "level":
        # FIXME: Somehow, this shows WARN even though -vvv is enabled.
        level = logging.getLogger().getEffectiveLevel()
        levels = ["notset", "debug [-vvv]", "info [-vv]",
                  "warn [-v]", "error, least verbose"]
        label = levels[level / 10]
        return bot.say(channel, "Log level is {} ({})."
                        .format(level / 10, label))
    else:
        if bot.factory.logs_enabled:
            return bot.say(channel,
                "Logs are enabled. Use {}logs off to disable."
                .format(bot.lead))
        else:
            return bot.say(channel,
                "Logs are disabled. Use {}logs on to disable."
                .format(bot.lead))


def command_me(bot, user, channel, args):
    "Displays information about the user."
    nick = get_nick(user)
    level = permissions(user)
    return bot.say(channel, "{}, your permission level is {}.".format(nick,
                                                                      level))


def command_version(bot, user, channel, args):
    "Displays the current bot version."
    return bot.say(channel, "demibot v{} ({})".format(bot.factory.VERSION,
                                                      bot.factory.URL))


def command_printvars(bot, user, channel, args):
    "Displays instance variables of the client."
    if bot.factory.mininum_permissions > permissions(user) < 20:
        return bot.say(channel, "{}, insufficient permissions.".format(
                       get_nick(user)))

    return bot.say(channel, "pw: {}, rn: {}, un: {}, ui: {}, lR: {}, hn: {}"
                   .format(bot.password, bot.realname, bot.username,
                           bot.userinfo, bot.lineRate, bot.hostname))


def command_ping(bot, user, channel, args):
    "Dummy command. Try it!"
    return bot.say(channel, "{}, Pong.".format(get_nick(user)))
