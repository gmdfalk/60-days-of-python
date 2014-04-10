#!/usr/bin/env python2
# TODO:
# Database (User info, channel stats, quiz, permission levels, alternate nicks)
# Modules: Seen+Tell, RSS+Github, IMDB/TVcal, Twitter, madcow
# Replace logging with syslog
# Add support for channelpasswords
"""demibot - A multipurpose IRC bot (depends on twisted and requests)

Usage:
    demibot [<server> <channels>] [-a <adm>] [-n <nick>] [-p <pass>] [-l <dir>]
            [--ssl] [--no-logs] [-q] [-v...] [-h]

Arguments:
    server:port        Server to connect to, default port is 6667.
                       If you don't specify a server, demibot will use
                       config.py as connection information instead.
    channels           Channels to join, comma separated. Hash not necessary.

Options:
    -a, --admin=<adm>   The root admin for the bot.
    -n, --nick=<nick>   Nickname of the bot. [default: demibot]
    -p, --pass=<pass>   NickServ password, if required.
    -l, --logdir=<dir>  File to log bot events to.
    --no-logs           Turns off all file logging.
    -s, --ssl           Enable if the server supports SSL connections.
    -h, --help          Show this help message and exit.
    -q, --quiet         Do not log bot events to stdout (only to a file).
    -v                  Logging verbosity, up to -vvv.
"""

import os
import sys

from docopt import docopt
from twisted.internet import reactor, ssl

import config
from factory import Factory
from reporting import init_syslog


def main():
    args = docopt(__doc__, version="0.1")

    # If ~/.demibot or ~/.config/demibot exist, we use that as location for
    # the logs and auth file.
    configdir = os.path.dirname(os.path.realpath(__file__))  # We are here.
#     if not args["<server>"] and not args["--logdir"]:
    home = os.path.join(os.path.expanduser("~"), ".demibot")
    homeconfig = os.path.join(os.path.expanduser("~"), ".config/demibot")
    if os.path.isdir(homeconfig):
        configdir = homeconfig
    elif os.path.isdir(home):
        configdir = home

    # If no --logdir is specified, use the path to the running script + "logs".
    if not args["--logdir"]:
        args["--logdir"] = os.path.join(configdir, "logs")

    # Check if we have write permissions to the logdir and create it,
    # if necessary.
    try:
        os.makedirs(args["--logdir"])
    except OSError as e:
        # If the error number is anything but 13 we assume we have write
        # permissions.
        if e.errno == 13:  # Permission denied
            # No write permissions. Turn off all file logging.
            args["--no-logs"] = True
            print "Disabling file logging (no write permissions): OSError", e

    # If there is no server argument, read the connection infos from config.py.
    if not args["<server>"]:
        networks = config.create_options(configdir)
    # Otherwise we turn the docopt args into a config.py compatible format.
    else:
        # The default identity to connect with if we're not using config.py.
        identities = {
            "default": {
                "nickname": args["--nick"],
                "realname": "demibot",
                "username": args["--nick"],
                "nickserv_pw": args["--pass"],
            }
        }
        # Split server argument into server and port, if necessary.
        if ":" in args["<server>"]:
            args["<server>"], args["--port"] = args["<server>"].split(":")
        else:
            args["--port"] = "6667"
        # Use the longest string in the <server> arg as name for the network.
        # Let's hope this doesn't produce unexpected results.
        network_name = max(args["<server>"].split("."), key=len)
        # Fix channel names, if a hash is missing.
        try:
            channels = {i if i.startswith("#") else "#" + i\
                        for i in args["<channels>"].split(",")}
        except AttributeError:
            print "Could not resolve channel arguments."
            print "Syntax: demibot irc.freenode.net chan1,chan2,#chan3"
            sys.exit(1)
        networks = {
            network_name: {
                "server": args["<server>"],
                "port": int(args["--port"]),
                "ssl": args["--ssl"],
                "password": None,  # Server password, if you need one.
                "identity": identities["default"],
                "superadmins": {args["--admin"]},
                "admins": {},
                "channels": channels,
            }
        }

    # Cap verbosity count at 3 to avoid index errors.
    if args["-v"] > 3:
        args["-v"] = 3
    print args, configdir
    # Set up our logger for system events. Chat is logged separately.
    # Both will be disabled if --no-logs is True.
    init_syslog(args["--logdir"], args["-v"], args["--no-logs"], args["--quiet"])
    # Set up the connection info for each network.
    for name in networks.keys():

        f = Factory(name, networks[name], configdir, args["--logdir"],
                    args["--no-logs"])

        server = networks[name]["server"]
        port = networks[name]["port"]

        # Create a connection (using SSL, if enabled).
        if networks[name]["ssl"]:
            reactor.connectSSL(server, port, f, ssl.ClientContextFactory())
        else:
            reactor.connectTCP(server, port, f)

    # Finally, run all the factories/bots.
    reactor.run()

if __name__ == "__main__":
    main()
