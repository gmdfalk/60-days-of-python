
def handle_userJoined(bot, user, channel):
    "Automatically give operator status to admins"
    print "handle userjoined"
    if permissions(user) >= 10:
        print "permissions", user
        bot.log.info("Auto-OP for {}".format(user))
        bot.mode(channel, True, 'o', user=get_nick(user))
