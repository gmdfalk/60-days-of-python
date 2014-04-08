"""Core Commands

    The basic bot commands.

    These require admin rights:
        * join
        * leave
        * channels
        * quit
        * logs
        * rehash

    These don't:
        * help
        * version

    Most of these require admin rights.
"""

import logging

from twisted.python import rebuild


log = logging.getLogger("core")


def command_admins(bot, user, channel, args):
    "Add, remove or list admins. Usage: admins [(add|del) <nick>,...]"
    if permissions(user) < 20:
        return

    superadmins = set(bot.factory.network["superadmins"])
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
                bot.factory.network["admins"].add(i)
                bot.say(channel, "Added {} to admins.".format(i))
                log.debug("Added {} to admins.".format(i))
        else:
            bot.factory.network["admins"].add(args[1])
            bot.say(channel, "Added {} to admins.".format(args[1]))
            log.debug("Added {} to admins.".format(args[1]))


def command_rehash(bot, user, channel, args):
    "Rehashes all available modules to reflect any changes."

    if permissions(user) < 10:  # 10 == admin, 20 == superadmin
        return

    try:
        log.info("Rebuilding {}".format(bot))
        rebuild.updateInstance(bot)
        bot.factory._unload_removed_modules()
        bot.factory._loadmodules()
    except Exception, e:
        log.error("Rehash error: {}".format(e))
        return bot.say(channel, "Rehash error: {}".format(e))
    else:
        log.info("Rehash OK")
        return bot.say(channel, "Rehash OK")


def command_quit(bot, user, channel, args):
    "Ends this or optionally all client instances. Usage: quit [all]."

    if permissions(user) < 20:  # 10 == admin, 20 == superadmin
        return

    if args == "all":
        from twisted.internet import reactor
        reactor.stop()

    bot.factory.retry_enabled = False
    log.info("Received quit command for {} from {}. Bye."
             .format(bot.factory.network_name, user))
    bot.quit()


def command_join(bot, user, channel, args):
    "Usage: join <channel>,... (Comma separated, hash not required)."

    if permissions(user) < 10:  # 10 == admin, 20 == superadmin
        return

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

    if permissions(user) < 10:  # 10 == admin, 20 == superadmin
        return

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
    if permissions(user) < 10:  # 10 == admin, 20 == superadmin
        return

    return bot.say(channel, "I am on {}"
                    .format(",".join(bot.factory.network["channels"])))


def command_help(bot, user, channel, cmnd):
    "Get help on all commands or a specific one. Usage: help [<command>]"

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
    if permissions(user) < 20:  # 10 == admin, 20 == superadmin
        return

    if args == "off" and bot.factory.logs_enabled:
        bot.chatlogger.close_logs()
        bot.factory.logs_enabled = False
        log.debug("Chatlogs enabled")
        return bot.say(channel, "Chatlogs are now disabled.")
    elif args == "on" and not bot.factory.logs_enabled:
        bot.chatlogger.open_logs(bot.factory.network["channels"])
        bot.factory.logs_enabled = True
        log.debug("Chatlogs disabled")
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
    pass


def command_version(bot, user, channel, args):
    "Displays the current bot version."
    return bot.say(channel,
                   "demibot v{} (https://github.com/mikar/demibot)"
                   .format(bot.factory.VERSION))


def command_ping(bot, user, channel, args):
    "Dummy command. Try it!"
    return bot.say(channel,
                    "{}, Pong.".format(bot.factory.get_nick(user)))
