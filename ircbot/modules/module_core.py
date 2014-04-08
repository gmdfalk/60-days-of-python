import logging

from twisted.python import rebuild


log = logging.getLogger("client")



def command_rehash(bot, user, channel, args):
    "Rehashes all available modules to reflect any changes."

    # Only allow superadmins to reload modules.
    if bot.factory.is_superadmin(user):
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
    else:
        return bot.say(channel, "Requires admin rights")


def command_quit(bot, user, channel, args):
    "Ends this or optionally all client instances. Usage quit [all]"

    if not bot.factory.is_superadmin(user):
        return

    bot.factory.lost_delay = 0
    bot.quit()


def command_join(bot, user, channel, args):
    "Usage: join <channel>... (Comma separated, hash not required)"

    if not bot.factory.is_admin(user):
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
    "Usage: leave <channel>... (Comma separated, hash not required)"

    if not bot.factory.is_admin(user):
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
            bot.part(c)
        else:
            bot.say(channel, "I am not in {}".format(c))
            log.debug("Attempted to leave a channel i'm not in: {}"
                      .format(c))

        log.debug("Channels I'm in: {}"
                  .format(", ".join(network["channels"])))


def command_channels(bot, user, channel, args):
    "List channels the bot is on. No arguments."

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
    "Usage: logs [<on>|<off>|<level>]"
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
        levels = ["ERROR (default)", "WARN [-v]", "INFO [-vv]", "DEBUG [-vvv]"]
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


def command_ping(bot, user, channel, args):
    "Dummy command. Try it!"
    return bot.say(channel,
                    "{}, Pong.".format(bot.factory.get_nick(user)))
