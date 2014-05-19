# -*- coding: utf-8 -*-
"""Google Translate Module

    From https://github.com/EArmour/pyfibot/
"""
import logging


log = logging.getLogger("trans")

try:
    import requests
except ImportError:
    log.error("Missing requests library. The translate module won't work.")


gturl = "http://translate.google.com/translate_a/t"
gtheaders = {
             "User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64; rv:27.0)"\
             "Gecko/20100101 Firefox/27.0"
             }
gtbody = "client=gtranslate&sl=&tl=en&text=%s"


def command_translate(bot, user, channel, args):
    """Transliterates text with Google Translate to English.
    Usage: translate <text>."""
    gtrans = requests.post(gturl, data=gtbody % args, headers=gtheaders)
    json = gtrans.json()
    translated = json["sentences"][0]["trans"]
    bot.say(channel, "From " + json["src"] + ": " + translated)


def command_transliterate(bot, user, channel, args):
    """Transliterates text with Google Translate to English.
    Usage: transliterate <text>."""
    gtrans = requests.post(gturl, data=gtbody % args, headers=gtheaders)
    json = gtrans.json()
    transliterated = json["sentences"][0]["src_translit"]
    if transliterated == "":
        bot.say(channel, "No transliteration available.")
    else:
        bot.say(channel, "From " + json["src"] + ": " + transliterated)
