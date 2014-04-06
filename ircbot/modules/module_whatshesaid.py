from __future__ import unicode_literals, print_function
import random
   
def command_whatshesaid(bot, user, channel, args):
    """Calculates your body mass index. Usage: bmi height(cm)/weight(kg)"""
    quotesfile = "modules/whatshesaid.txt"
    with open(quotesfile) as f:
        self.quotes = f.readlines()
        print(self.quotes)
    quote = random.choice(self.quotes).strip()
    print(quote)
    return bot.say(channel, quote)
