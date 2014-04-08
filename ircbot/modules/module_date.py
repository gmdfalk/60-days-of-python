import datetime


def command_date(bot, user, channel, args):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
            "Saturday", "Sunday"]

    today = datetime.datetime.today().weekday()

    if args == "today":
        bot.say(channel, "Today is {}".format(days[today]))
    else:
        bot.say(channel, "Tomorrow is {}.".format(days[today + 1]))
