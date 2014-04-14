# -*- coding: utf-8 -*-
"""Generates a random name

    https://github.com/EArmour/pyfibot/
"""

import logging
from random import choice
import urllib

from bs4 import BeautifulSoup as bs4


log = logging.getLogger("rname")

api = "http://www.behindthename.com/api/random.php?usage=%s&gender=%s&randoms\
urname=yes&number=1&key=ev465701"

def command_randomname(bot, user, channel, args):
    """Generates a random name of the specified type from BehindTheName.com.
    See country codes at: http://www.behindthename.com/api/appendix2.php
    Usage: randomname <country> [<gender>]."""

    if args == "help":
        return bot.say(channel, "Usage: randomname <country> [<gender>].")

    countries = {
        "African": "afr",
        "Akan": "aka",
        "Albanian": "alb",
        "Algonquin": "alg",
        "Native American": "ame",
        "Amharic": "amh",
        "Ancient": "anci",
        "Apache": "apa",
        "Arabic": "ara",
        "Armenian": "arm",
        "Astronomy": "astr",
        "Indigenous Australian": "aus",
        "Aymara": "aym",
        "Azerbaijani": "aze",
        "Basque": "bas",
        "Bengali": "ben",
        "Berber": "ber",
        "Biblical": "bibl",
        "Bosnian": "bos",
        "Breton": "bre",
        "Bulgarian": "bul",
        "Catalan": "cat",
        "Ancient Celtic": "cela",
        "Celtic Mythology": "celm",
        "Chinese": "chi",
        "Choctaw": "cht",
        "Comanche": "com",
        "Coptic": "cop",
        "Cornish": "cor",
        "Cree": "cre",
        "Croatian": "cro",
        "Corsican": "crs",
        "Czech": "cze",
        "Danish": "dan",
        "Dutch": "dut",
        "English": "eng",
        "Esperanto": "esp",
        "Estonian": "est",
        "Ewe": "ewe",
        "Fairy": "fairy",
        "Filipino": "fil",
        "Finnish": "fin",
        "Flemish": "fle",
        "French": "fre",
        "Frisian": "fri",
        "Galician": "gal",
        "Ganda": "gan",
        "Georgian": "geo",
        "German": "ger",
        "Goth": "goth",
        "Greek": "gre",
        "Ancient Greek": "grea",
        "Greek Mythology": "grem",
        "Greenlandic": "grn",
        "Hawaiian": "haw",
        "Hillbilly": "hb",
        "Hippy": "hippy",
        "History": "hist",
        "Hungarian": "hun",
        "Ibibio": "ibi",
        "Icelandic": "ice",
        "Igbo": "igb",
        "Indian": "ind",
        "Indian Mythology": "indm",
        "Indonesian": "ins",
        "Inuit": "inu",
        "Iranian": "ira",
        "Irish": "iri",
        "Iroquois": "iro",
        "Italian": "ita",
        "Japanese": "jap",
        "Jewish": "jew",
        "Kazakh": "kaz",
        "Khmer": "khm",
        "Kikuyu": "kik",
        "Kreatyve": "kk",
        "Korean": "kor",
        "Kurdish": "kur",
        "Kyrgyz": "kyr",
        "Latvian": "lat",
        "Limburgish": "lim",
        "Literature": "lite",
        "Lithuanian": "lth",
        "Luhya": "luh",
        "Luo": "luo",
        "Macedonian": "mac",
        "Maltese": "mal",
        "Manx": "man",
        "Maori": "mao",
        "Mapuche": "map",
        "Mayan": "may",
        "Medieval": "medi",
        "Mongolian": "mon",
        "Mormon": "morm",
        "Mwera": "mwe",
        "Mythology": "myth",
        "Nahuatl": "nah",
        "Navajo": "nav",
        "Ndebele": "nde",
        "Norwegian": "nor",
        "Nuu-chah-nulth": "nuu",
        "Occitan": "occ",
        "Ojibwe": "oji",
        "Pacific/Polynesian": "pac",
        "Pakistani": "pak",
        "Pet": "pets",
        "Polish": "pol",
        "Popular Culture": "popu",
        "Portuguese": "por",
        "Punjabi": "pun",
        "Quechua": "que",
        "Rapper": "rap",
        "Romanian": "rmn",
        "Ancient Roman": "roma",
        "Roman Mythology": "romm",
        "Russian": "rus",
        "Sami": "sam",
        "Norse Mythology": "scam",
        "Scottish": "sco",
        "Serbian": "ser",
        "Shawnee": "sha",
        "Shona": "sho",
        "Sioux": "sio",
        "Norse Mythology": "slam",
        "Slovak": "slk",
        "Slovene": "sln",
        "Sotho": "sot",
        "Spanish": "spa",
        "Swahili": "swa",
        "Swedish": "swe",
        "Tagalog": "tag",
        "Tamil": "tam",
        "Telugu": "tel",
        "Ancient Germanic": "teua",
        "Thai": "tha",
        "Theology": "theo",
        "Tibetan": "tib",
        "Transformer": "trans",
        "Tswana": "tsw",
        "Tumbuka": "tum",
        "Turkish": "tur",
        "Ukrainian": "ukr",
        "?": "unkn",
        "Urdu": "urd",
        "American": "usa",
        "Various": "vari",
        "Vietnamese": "vie",
        "Welsh": "wel",
        "Witch": "witch",
        "Wrestler": "wrest",
        "Xhosa": "xho",
        "Yao": "yao",
        "Yoruba": "yor",
        "Zapotec": "zap",
        "Zulu": "zul",
    }

    args = args.split()
    if len(args) > 2:
        return bot.say(channel, "Usage: randomname <country> [<gender>].")
    elif len(args) == 2:
        gender = args[1]
    else:
        gender = "both"

    genders = ["m", "f", "both"]
    if gender not in genders:
        return bot.say(channel, "Valid genders are m, f or both.")

    if not args:
        country, gender = choice(countries.keys()).lower(), choice(genders)
    else:
        country = args[0].lower()

    match_found = False
    for long, short in countries.items():
        long, short = long.lower(), short.lower()
        # We use very lose matching.
        if country in long or country in short:
            country_code = short
            country_text = long
            match_found = True
            break

    if not match_found:
        return bot.say(channel, "No match found for '{}'".format(country))

    if gender == "m":
        gender_text = "a man"
    elif gender == "f":
        gender_text = "a woman"
    else:
        gender_text = "both genders"

    data = urllib.urlopen(api % (country_code, gender))
    parsed = bs4(data, "xml")

    return bot.say(channel, "Random {} name for {}: {}"
                   .format(country_text, gender_text,
                           parsed.get_text().encode('utf8').strip()))
