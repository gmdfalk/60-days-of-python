import random

def command_swanson(bot, user, channel, args):
    """Calculates your body mass index. Usage: bmi height(cm)/weight(kg)"""
    with open("modules/swanson.txt") as f:
        quotes = f.readlines()
    quote = random.choice(quotes).strip()
    return bot.say(channel, quote)
