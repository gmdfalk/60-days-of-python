import logging

from twisted.internet import reactor


log = logging.getLogger("channels")
delay = 60


def handle_kickedFrom(bot, channel, kicker, message):
    "Rejoin channel after <delay> seconds."

    log.info("Kicked from {} by {}. Reason: {}".format(kicker, channel, message))
    log.info("Rejoining in {} seconds".format(delay))
    bot.factory.network["channels"].discard(channel)
    reactor.callLater(delay, bot.join, channel)


def handle_userJoined(bot, user, channel):
    """Rejoin a channel if i was redirected but add a delay to avoid hammering.
    Primarily useful, if we tried to join a channel before being identified by
    NickServ"""
    if channel == "#python-unregistered":
        bot.leave(channel)
        bot.factory.network["channels"].discard(channel)
        reactor.callLater(delay, bot.join, "#python")
