from twisted.internet import defer, reactor


def command_timer(self, user, channel, args):
    "Repeats a message after n seconds. Usage: timer <n> <message>"
    delay, _, msg = args.partition(" ")

    try:
        delay = int(delay)
    except ValueError:
        pass

    d = defer.Deferred()
    msg = self.say(channel, "{}, {}".format(get_nick(user), msg))

    return reactor.callLater(delay, d.callback, msg)
