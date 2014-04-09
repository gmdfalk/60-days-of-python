
def get_cx(cx_id=None):
    "Reads Google Search ID from a file."
    try:
        with open(".auth") as f:
            authlist = f.readlines()
    except IOError:
        cx_id = None
    else:
        cx_id = [i.split() for i in authlist if i.startswith("cx ")][0]

    return cx_id[1]

def command_g(bot, user, channel, args):
    "Searches Google and returns the first result. Usage: g <string>"
    # FIXME: Add correct site to CX_ID.

    cx = get_cx()
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
