
def handle_userJoined(bot, user, channel):
    "Automatically give operator status to admins"
    print "handle userjoined"
    if permissions(user) >= 10:
        bot.mode(channel, True, 'o', user=get_nick(user))
