import re


def read_quizfile(quizfile):
    "Reads the quizfile into a big dictionary."
    try:
        with open(quizfile) as f:
            linelist = f.readlines()
    except IOError:
        quizdict = None
    else:
        for line in linelist:
            if ":" in line:
                line = line.split(":")
                category = line[0]

    return quizdict


def command_quiz(bot, user, channel, args):
    "Calculates your body mass index. Usage: bmi height(cm)/weight(kg)"
    data = args.split("/")
    if len(data) != 2:
        return bot.say(channel, "Usage: bmi height(cm)/weight(kg)")
    else:
        bmi = print_bmi(calc_bmi(int(data[0]), int(data[1])))
        return bot.say(channel, "{}, {}".format(get_nick(user), bmi))
