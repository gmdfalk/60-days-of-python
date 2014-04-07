#!/usr/bin/env python2
"""demibot - A multipurpose IRC bot

Usage:
    demibot [<server> <channels>] [-n <nick>] [-p <pass>] [-m N] [-s]
            [-q] [-h] [-v...]

Arguments:
    server:port        Server to connect to, default port is 6667.
                       If you don't specify a server, demibot will use
                       config.py as connection information instead.
    channels           Channels to join, comma separated. Hash not necessary.

Options:
    -n, --nick=<nick>  Nickname of the bot [default: demibot]
    -p, --pass=<pass>  NickServ password, if required.
    -s, --ssl          Enable if the server supports SSL connections.
    -m, --max-tries N  Limit retries on network errors. [default: 4]
    -h, --help         Show this help message and exit.
    -q, --quiet        Do not pipe log messages to stdout.
    -v                 Logging verbosity, up to -vvv.

Examples:
    demibot irc.freenode.net:6667 freenode,archlinux
    demibot irc.freenode.net #django,#python -n demibot --ssl
    demibot  (uses config.py for multiserver support with detailed settings)
"""

import logging
import sys

from docopt import docopt
from twisted.internet import reactor, ssl

import config
from factory import Factory
from reporting import init_logging


log = logging.getLogger("main")


def main():
    args = docopt(__doc__, version="0.1")
    print args["-v"]
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
                "realname": "Anonymous",
                "username": "test",  # args["--nick"],
                "nickserv_pw": args["--pass"],
            }
        }
        servername = args["<server>"].split(".")[1]  # Let's hope this works.
        networks = {
            servername: {
                "server": args["<server>"],
                "port": int(args["--port"]),
                "ssl": args["--ssl"],
                "identity": identities["default"],
                "admins": ["mikar", "pld"],
                "channels": channels,
            }
        }

    # Logging setup.
    if not args["--quiet"]:
        pass

    # Cap verbosity count at 3 so we don't get index errors.
    if args["-v"] > 3:
        args["-v"] = 3

    # Set up our logger.
    init_logging(args["-v"])

    # Set up the connection info for each network.
    for name in networks.keys():

        factory = Factory(name, networks[name], args["-v"])

        server = networks[name]["server"]
        port = networks[name]["port"]

        # Create a connection depending on whether SSL is enabled.
        if networks[name]["ssl"]:
            reactor.connectSSL(server, port, factory,
                               ssl.ClientContextFactory())
        else:
            reactor.connectTCP(server, port, factory)

    # Finally, run all the factories/bots.
    reactor.run()

if __name__ == "__main__":
    main()
