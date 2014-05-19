import logging
import os
import random


log = logging.getLogger("quotes")


def command_swanson(bot, user, channel, args):
    "Prints Ron Swanson quotes."
    quotefile = os.path.join(bot.factory.moduledir, "swanson.txt")

    try:
        with open(quotefile) as f:
            quotes = f.readlines()
    except IOError:
        log.error("Could not read {}".format(quotefile))
    else:
        quote = random.choice(quotes).strip()

    return bot.say(channel, "{} - Ron Swanson".format(quote))


def command_whatshesaid(bot, user, channel, args):
    "Prints quotes of accomplished women."
    quotefile = os.path.join(bot.factory.moduledir, "whatshesaid.txt")

    try:
        with open(quotefile) as f:
            quotes = f.readlines()
    except IOError:
        log.error("Could not read {}".format(quotefile))
    else:
        quote = random.choice(quotes).strip()

    return bot.say(channel, quote)
