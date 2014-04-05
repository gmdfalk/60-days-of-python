#!/usr/bin/env python2
"""IRCBot

Usage:
    ircbot.py [-h] [-s <server>] [-p <port>] [--password=<pass>] [-c <chans>]
              [-n <nick>] [-o <file>] [--ssl] [--max-tries N] [-v N] [-q]

Options:
    -s, --server=<server>    DNS address [default: irc.freenode.net]
    -p, --port=<port>        Port number of the IRC server [default: 6667]
    -pw, --password=<pass>   Server password, if required
    -c, --channels=<chans>   Channels, comma separated [default: z1,z2,z3]
    -n, --nick=<nick>        Nickname of the bot [default: maxbot]
    -o, --output=<file>      Logging file [default: test.log]
    --max-tries N            Limit retries on network errors [default: 4]
    --ssl                    Whether to use SSL.
    -h, --help               Show this help msg and exit
    -v, --verbose N          Verbose logging (0-3) [default: 1]
    -q, --quiet              Quiet logging
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
import sys

import settings
import client


def main():

    # For multiple server support, set this to True and modify settings.py.
    use_settings = False

    args = docopt(__doc__, version="0.1")

    if use_settings:
        networks = settings.networks
    else:
        channels = [i if i.startswith("#") else "#" + i\
                         for i in args["--channels"].split(",")]
        identity = {
            'Identity': {
                'nickname': args["--nick"],
                'realname': 'None',
                'username': 'None',
                'nickserv_pw': None
            }
        }
        networks = {
            'Server': {
                'server': args["--server"],
                'port': int(args["--port"]),
                'ssl': args["--ssl"],
                'identity': identity["Identity"],
                'channels': tuple(channels)
            }
        }
    logfile = args["--output"]

    if not args["--quiet"]:
        client.log.startLogging(sys.stdout)

    for name in networks.keys():
        factory = client.Factory(name, networks[name])

        server = networks[name]['server']
        port = networks[name]['port']

        if networks[name]['ssl']:
            client.reactor.connectSSL(server, port, factory,
                                      client.ssl.ClientContextFactory())
        else:
            client.reactor.connectTCP(server, port, factory)

    client.reactor.run()

if __name__ == "__main__":
    main()
