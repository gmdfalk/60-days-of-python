import logging
import subprocess
import os


log = logging.getLogger("update")


def command_update(bot, user, channel, args):
    """Update the bot sources from our github repository. Depending on your
    git configuration you might have to enter a password in the console."""
    # TODO: Add interactive(chat) password entry.
    if permissions(user) < 20:
        return

    cmd = ["git", "pull"]
    cwd = os.getcwd()

    log.debug("Executing git pull in {}.".format(cwd))

    p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    res = p.wait()
    out, err = p.communicate()

    if res:
        bot.say(channel, "Update failed.")
    else:
        bot.say(channel, "Update OK.")
    for line in out.split("\n"):
        bot.say(channel, "{}".format(line))
    if err:
        bot.say(channel, "Errors: {}".format(err))