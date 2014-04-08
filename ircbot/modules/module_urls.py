import logging


log = logging.getLogger("urls")


def command_urls(bot, user, channel, args):
    "Prints the titles of URLs linked in the channel. Usage: urls [on|off]"
    if permissions(user) < 10:  # 10 == admin, 20 == superadmin
        return

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
                "URL title display is enabled. Use {}urls off to disable."
                .format(bot.lead))
        else:
            return bot.say(channel,
                "URL title display is disabled. Use {}urls on to enable."
                .format(bot.lead))
