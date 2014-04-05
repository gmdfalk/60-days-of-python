#!/usr/bin/env python2
"""demibot - A multipurpose IRC bot

Usage:
    demibot [<server> <channels>] [-n <nick>] [-p <pass>] [-f <file>]
            [-m N] [-s] [-q] [-h] [-v...]

Arguments:
    server:port        Server to connect to, default port is 6667.
                       If you don't specify a server, demibot will use
                       config.py as connection information instead.
    channels           Channels to join, comma separated.

Options:
    -n, --nick=<nick>  Nickname of the bot [default: demibot]
    -f, --file=<file>  Name of the logging file. [default: demibot.log]
    -s, --ssl          Enable if the server supports SSL connections.
    -p, --pass=<pass>  NickServ password, if required.
    -m, --max-tries N  Limit retries on network errors. [default: 4]
    -h, --help         Show this help message and exit.
    -q, --quiet        Do not pipe log messages to stdout.
    -v                 Logging verbosity, up to -vvv.

Examples:
    demibot irc.freenode.net:6667 freenode,archlinux
    demibot irc.freenode.net #django,#python -n demibot --ssl
    demibot    (will use information in config.py to connect)
"""

# Possible features:
# HTTP link capture/collection and saving or displaying the title in chat
# Weather and date/time information (day + week number, too)
# Quiz (smart autohinting, highscores, etc)
# Collecting/displaying quotes (Chirpy?)
# Store notes with keyword and repeat them on demand (!give nick note)
# Google search (or other services, like translate)
# Operator/Auth features (Kick, Ban, automatically give OP)
# Disable/enable commands, public ignore
# Fortune cookies, Ron swanson quotes
# Seen (track last msg by user x)
# Conduct a poll.
# Evaluate python/bash
# Dictionary, wiki
# Search channel log.
# msg system (leaving a notification)

# TODO:
# 1. reading password information from a file instead of config.py
# 2. log to database


from docopt import docopt
import logging
import sys

import config
import client


def main():

    # Establish the configuration.
    if not args["<server>"]:
        networks = config.networks
    else:
        # Fix channel names, if a hash is missing.
        channels = [i if i.startswith("#") else "#" + i\
                    for i in args["<channels>"].split(",")]
        # Split server argument into server and port, if necessary.
        if ":" in args["<server>"]:
            args["<server>"], args["--port"] = args["<server>"].split(":")
        else:
            args["--port"] = "6667"

        # Turn the docopt args dict into a config.py compatible format.
        # Editing this is only necessary if yo
        identities = {
            "default": {
                "nickname": args["--nick"],
                "realname": "Anyonymous",
                "username": args["--nick"],
                "nickserv_pw": args["--pass"],
            }
        }
        networks = {
            "default": {
                "server": args["<server>"],
                "port": int(args["--port"]),
                "ssl": args["--ssl"],
                "identity": identities["default"],
                "channels": tuple(channels)
            }
        }

    # Logging setup.
    logfile = args["--file"]
    if not args["--quiet"]:
        client.log.startLogging(sys.stdout)

    # Cap verbosity count at 3 so we don't get index errors.
    if args["-v"] > 3:
        args["-v"] = 3
    # Set the log level according to verbosity count.
    levels = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
    logging.basicConfig(level=levels[args["-v"]])

    print args
    # Set up the connection info for each network.
    for name in networks.keys():
        factory = client.Factory(name, networks[name])

        server = networks[name]["server"]
        port = networks[name]["port"]

        if networks[name]["ssl"]:
            client.reactor.connectSSL(server, port, factory,
                                      client.ssl.ClientContextFactory())
        else:
            client.reactor.connectTCP(server, port, factory)

    # Run all the factories/bots.
    client.reactor.run()

if __name__ == "__main__":
    args = docopt(__doc__, version="0.1")
    main()
