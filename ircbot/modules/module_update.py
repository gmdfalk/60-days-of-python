import logging
import os
import subprocess


log = logging.getLogger("update")


def command_update(bot, user, channel, args):
    """Update the bot sources from our github repository. Depending on your
    git configuration you might have to enter a password in the console."""
    # TODO: Add interactive(chat) password entry (also need for quizzing).
    if permissions(user) < 20:
        return bot.say(channel, "Insufficient permissions.")

    cmd = ["git", "pull"]
    cwd = bot.factory.basedir

    log.debug("Executing git pull in {}.".format(cwd))

    p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    res = p.wait()
    out, err = p.communicate()

    if res:
        bot.say(channel, "Update failed.")
        log.info("Update failed.")
    else:
        bot.say(channel, "Update OK.")
        log.info("Update OK.")
    for line in out.split("\n"):
        bot.say(channel, "{}".format(line))
    if err:
        bot.say(channel, "Errors: {}".format(err))