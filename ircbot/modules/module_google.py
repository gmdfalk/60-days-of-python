import re


def get_cx(cx_id=None):
    "Reads Google Search ID from a file."
    try:
        with open(".auth") as f:
            authstr = f.read()
    except IOError:
        cx_id = None
    else:
        cx_id = re.search("(?<=cx ).*", authstr)
        if cx_id:
            cx_id = cx_id.group()

    return cx_id

def command_g(bot, user, channel, args):
    "Searches Google and returns the first result. Usage: g <string>"
    # FIXME: Add correct site to CX_ID.

    cx = get_cx()
    print
    print cx
    print
    if not cx:
        return

    url = "https://www.googleapis.com/customsearch/v1?q=%s&cx=%s&num=1&safe"\
          "=off&key=AIzaSyCaXV2IVfhG1lZ38HP7Xr9HzkGycmsuSDU"

    if not args:
        return bot.say(channel, "No search query!")

    search = get_urlinfo(url % (args, cx))
    parsed = search.json()

    results = parsed["searchInformation"]["totalResults"]

    if results == "0":
        return bot.say(channel, "Google found nothing for query: {}"
                       .format(args))

    first_url = parsed["items"][0]["link"]
    title = parsed["items"][0]["title"]

    bot.say(channel, "Google: {} - {}".format(title, first_url))
