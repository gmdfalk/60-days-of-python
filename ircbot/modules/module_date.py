import datetime
from dateutil.tz import tzlocal


def command_date(bot, user, channel, args):
    "Shows date information. Usage: date [now|epoch]"
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
            "Saturday", "Sunday"]

    d = datetime.datetime.now(tzlocal())
    tomorrow = days[d.weekday() + 1]
    n = d.strftime("%Z/UTC%z: %H:%M:%S, %Y-%m-%d (%A, %j/%U)")

    if args == "now":
        bot.say(channel, n)
    elif args == "epoch":
        bot.say(channel, "{}".format(d.strftime("%ss since 01.01.1970")))
    else:
        bot.say(channel, "Tomorrow is {}.".format(tomorrow))
