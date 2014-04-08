import logging
log = logging.getLogger("titles")


def command_titles(bot, user, channel, args):
    "Prints the titles of URLs linked in the channel. Usage: titles [on|off]"
    if args == "off" and bot.factory.titles_enabled:
        bot.factory.titles_enabled = False
        log.debug("URL title display disabled.")
        return bot.say(channel, "URL title display is now disabled.")
    elif args == "on" and not bot.factory.titles_enabled:
        bot.factory.titles_enabled = True
        log.debug("URL title display enabled.")
        return bot.say(channel, "URL title display is now enabled.")
    else:
        if bot.factory.titles_enabled:
            return bot.say(channel,
                "URL title display is enabled. Use {}titles off to disable."
                .format(bot.lead))
        else:
            return bot.say(channel,
                "URL title display is disabled. Use {}titles on to enable."
                .format(bot.lead))