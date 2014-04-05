#!/usr/bin/env python2
"""IRCBot

Usage:
    main.py [-h] [-s <server>] [-p <port>] [-c <chans>] [-n <nick>] [-o <file>]
            [--password=<pass>] [--max-tries N] [--ssl] [-v...] [-q]

Options:
    -s, --server=<server>    DNS address of server. [default: irc.freenode.net]
    -p, --port=<port>        Port number of the IRC server. [default: 6667]
    -c, --channels=<chans>   Channels, comma separated. [default: z1,z2]
    -n, --nick=<nick>        Nickname of the bot [default: maxbot]
    -o, --output=<file>      Name of the logging file. [default: ircbot.log]
    -pw, --password=<pass>   Server password, if required. It rarely is.
    --max-tries N            Limit retries on network errors. [default: 4]
    --ssl                    Whether to use SSL.
    -h, --help               Show this help msg and exit.
    -q, --quiet              Do not pipe log messages to stdout.
    -v                       Logging verbosity, up to -vvv.
"""

# Possible features:
# HTTP link capture/collection and saving or displaying the title in chat
# Weather and date/time information (day + week number, too)
# Quiz
# Collecting/displaying quotes (Chirpy?)
# Store notes with keyword and repeat them on demand
# Google search (or other services, like translate)
# Operator/Auth features (Kick, Ban, automatically give OP)
# Disable/enable commands, public ignore
# Fortune cookies or something like that
# Seen (track last msg by user x)
# Conduct a poll.
# Evaluate python/bash
# Dictionary, wiki
# Search channel log.
# msg system (leaving a notification)


from docopt import docopt
import logging
import sys

import settings
import client


def main():

    # For multiple server support, set this to True and modify settings.py.
    use_settings = True

    args = docopt(__doc__, version="0.1")

    # Establish the settings.
    if use_settings:
        networks = settings.networks
    else:
        # Fix channel names if necessary.
        channels = [i if i.startswith("#") else "#" + i\
                         for i in args["--channels"].split(",")]

        #
        identities = {
            'default': {
                'nickname': args["--nick"],
                'realname': 'None',
                'username': 'None',
                'nickserv_pw': None
            }
        }
        networks = {
            'default': {
                'server': args["--server"],
                "port": int(args["--port"]),
                "ssl": args["--ssl"],
                "identity": identities["default"],
                "channels": tuple(channels)
            }
        }
    logfile = args["--output"]

    # Logging setup.
    if not args["--quiet"]:
        client.log.startLogging(sys.stdout)

    # Cap verbosity count at 3 so we don't get index errors.
    if args["--verbose"] > 3:
        args["--verbose"] = 3
    # Set the log level according to verbosity count.
    levels = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
    logging.basicConfig(level=levels[args["--verbose"]])

    # Set up the connection info for each network.
    for name in networks.keys():
        factory = client.Factory(name, networks[name])

        server = networks[name]['server']
        port = networks[name]['port']

        if networks[name]['ssl']:
            client.reactor.connectSSL(server, port, factory,
                                      client.ssl.ClientContextFactory())
        else:
            client.reactor.connectTCP(server, port, factory)

    # Run all the factories/bots.
    client.reactor.run()

if __name__ == "__main__":
    args = docopt(__doc__, version="0.1")
    print args
#     main()
