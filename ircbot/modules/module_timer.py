from twisted.internet import reactor


def command_timer(bot, user, channel, args):
    "Repeats a message after n seconds. Usage: timer <n> <message>"
    delay, _, msg = args.partition(" ")

    try:
        delay = int(delay)
    except ValueError:
        return bot.say(channel, "Error: Need a number as first argument.")

    reactor.callLater(delay, bot.say, channel, "{}, {}.".format(get_nick(user),
                                                                msg))
