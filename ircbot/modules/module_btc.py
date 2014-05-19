# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
"""Get bitcoin exchange rates.

    From https://github.com/EArmour
"""

def command_btc(bot, user, channel, args):
    """Display current BTC exchange rates from mtgox.
    Usage: btc [<currencycode>...]."""
    currencies = ["EUR"]

    if args:
        currencies = args.split()

    return bot.say(channel, get_coin_value(bot, "BTC", currencies))


def get_coin_value(bot, coin, currencies):

    rates = []

    for currency in currencies:
        rate = gen_string(bot, coin, currency)
        if rate:
            rates.append(rate)

    if rates:
        return "1 %s = %s" % (coin, " | ".join(rates))
    else:
        return None


def gen_string(bot, coin="BTC", currency="EUR"):
    r = get_urlinfo("http://data.mtgox.com/api/1/%s%s/ticker" % (coin,
                                                                 currency))

    if r.json()["result"] != "success":
        return None

    data = r.json()["return"]

    avg = data["avg"]["display_short"]
    low = data["low"]["display_short"]
    high = data["high"]["display_short"]
    vol = data["vol"]["display_short"]

    return "{} avg:{} low:{} high:{} vol:{}".format(currency.upper(), avg,
                                                    low, high, vol)
