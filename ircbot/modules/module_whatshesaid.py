import random

def command_whatshesaid(bot, user, channel, args):
    """Calculates your body mass index. Usage: bmi height(cm)/weight(kg)"""
    with open("modules/whatshesaid.txt") as f:
        quotes = f.readlines()
    quote = random.choice(quotes).strip()
    return bot.say(channel, quote)
