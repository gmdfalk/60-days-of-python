import os
import random
import re
import time

from twisted.internet import reactor
# TODO: Create a Quiz class and enable privmsg interaction.

def read_quizfile(quizfile):
    "Reads the quiz file into a big dictionary."
    try:
        with open(quizfile) as f:
            linelist = f.readlines()
    except IOError:
        questionlist = None
    else:
        questionlist = []
        # Splits the line into category:question*answers match groups.
        rgx = re.compile("(?:([^:]*):)?([^*]*)\*(.*)")
        for line in linelist:
            match = rgx.search(line)
            question = match.group(1), match.group(2), match.group(3)
            questionlist.append(question)

    return questionlist


def update_hint(factory):
    "Create a hint for an answer."
    hint = list(factory.hint)
    answer = factory.answer
    count = 0
    while count < 3:
        index = random.randrange(len(answer))
        if hint[index] == "_":
            hint[index] = answer[index]
            count += 1

    factory.hint = "".join(hint)


def command_quiz(bot, user, channel, args):
    "A very basic quiz bot. No hints, no points. Usage: quiz [on|off|<delay>]."
    # TODO:
    delay = 25

    if args == "hint" or args == "clue":
        update_hint(bot.factory)
        return bot.say(channel, bot.factory.hint)
    elif args == "on":
        bot.factory.quiz_enabled = True
        bot.say(channel, "Quiz is now enabled. Delay: {}.".format(delay))
    elif args == "off":
        bot.factory.quiz_enabled = False
        return bot.say(channel, "Quiz is now disabled.")
    elif args == "help":
        bot.say(channel, "Usage: quiz [on|off|<delay>].")
    elif args.isdigit() and not args > 60:
        delay = int(args)
        bot.say(channel, "Delay changed to: {}.".format(delay))
    else:
        bot.say(channel, "Quiz running: {}. Delay: {}"
                .format(bot.factory.quiz_enabled, delay))

    quizlist = None
    if bot.factory.quiz_enabled:
        quizfile = os.path.join(bot.factory.moduledir, "quiz_general.txt")
        quizlist = read_quizfile(quizfile)

    while bot.factory.quiz_enabled and quizlist:
        category, question, answers = random.choice(quizlist)
        question = question.strip().capitalize()  # Format the question poco.
        bot.factory.answer = answers.split("*")[0]
        bot.factory.hint = "".join(["_" if i != " " else " " for i in\
                                    bot.factory.answer])
        if category:
            bot.say(channel, "{}: {}?".format(category, question))
        else:
            bot.say(channel, "{}?".format(question))

        reactor.callLater(delay, bot.say, channel, answers)
        time.sleep(delay + 5)
