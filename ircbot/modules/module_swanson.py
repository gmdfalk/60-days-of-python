import random

def command_swanson(bot, user, channel, args):
    "Prints Ron Swanson quotes. No arguments"
    with open("modules/swanson.txt") as f:
        quotes = f.readlines()
    quote = random.choice(quotes).strip()
    return bot.say(channel, quote)
