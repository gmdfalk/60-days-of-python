import random

def command_whatshesaid(bot, user, channel, args):
    "Prints quotes of accomplished women. No arguments"
    with open("modules/whatshesaid.txt") as f:
        quotes = f.readlines()
    quote = random.choice(quotes).strip()
    return bot.say(channel, quote)
