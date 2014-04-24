#!/usr/bin/env python2
# TODO:
# Database (User info, channel stats, quiz, permission levels, alternate nicks)
# Modules: Seen+Tell, RSS+Github, IMDB/TVcal, Twitter, madcow, uptime
# Add support for channelpasswords
# Improve config file concept:
#     Maybe use environment variable to get config dir. That way, we can put
#     config.py there, too.
#     Or use ConfigParser with some tweaks and build the dictionary myself like
#     {sec:dict(cfg.items(sec)) for sec in cfg.sections()}.
#     Or use JSON.
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

from ConfigParser import SafeConfigParser
import os
import sys

from docopt import docopt
from twisted.internet import reactor, ssl

from factory import Factory
from reporting import init_logger


def get_configdir():
    # If ~/.demibot or ~/.config/demibot exist, we use that as source and
    # target for logs and config file.
    configdir = os.path.dirname(os.path.realpath(__file__))  # We are here.
#     if not args["<server>"] and not args["--logdir"]:
    home = os.path.join(os.path.expanduser("~"), ".demibot")
    homeconfig = os.path.join(os.path.expanduser("~"), ".config/demibot")
    if os.path.isdir(homeconfig):
        configdir = homeconfig
    elif os.path.isdir(home):
        configdir = home

    return configdir


def parse_config(configdir):
    config = SafeConfigParser()
    config.read(os.path.join(configdir, "demibot.ini"))
    networks = {}
    for s in config.sections():
        networks[s] = {k:v for k, v in config.items(s)}

    # Correct a couple of values.
    for n in networks:
        networks[n]["port"] = config.getint(n, "port")
        networks[n]["ssl"] = config.getboolean(n, "ssl")
        networks[n]["urltitles_enabled"] = config.getboolean(n, "urltitles_enabled")
        networks[n]["minperms"] = config.getint(n, "minperms")
        networks[n]["lost_delay"] = config.getint(n, "lost_delay")
        networks[n]["failed_delay"] = config.getint(n, "failed_delay")
        networks[n]["rejoin_delay"] = config.getint(n, "rejoin_delay")
        for k, v in networks[n].items():
            if k == "superadmins":
                networks[n]["superadmins"] = set(v.replace(" ", "").split(","))
            elif k == "admins":
                networks[n]["admins"] = set(v.replace(" ", "").split(","))
            elif k == "channels":
                networks[n]["channels"] = {i if i.startswith("#") else "#" + i\
                                           for i in v.replace(" ", "").split(",")}

    return networks


def main():
    configdir = get_configdir()

    if not args["--logdir"]:
        args["--logdir"] = os.path.join(configdir, "logs")

    # Check if we have write permissions to the logdir and create it,
    # if necessary.
    try:
        os.makedirs(args["--logdir"])
    except OSError as e:
        if e.errno == 13:  # Permission denied
            args["--no-logs"] = True
            print "ERROR: No write permissions ({}). Chatlogs off.".format(e)


    if not args["<server>"]:
        # If there is no server argument, read the connection information from
        # demibot.ini in configdir.
        networks = parse_config(configdir)
    else:  # Parse connection info from command-line.
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
            print "ERROR: Could not resolve channel arguments."
            print "Syntax: demibot irc.freenode.net chan1,chan2,#chan3"
            sys.exit(1)
        networks = {
            network_name: {
                "server": args["<server>"],
                "port": int(args["--port"]),
                "ssl": args["--ssl"],
                "nickname": args["--nick"],
                "nickserv_pw": args["--pass"],
                "superadmins": {args["--admin"]} or set(),
                "admins": set(),
                "channels": channels,
            }
        }

    # Set up our logger for system events. Chat is logged separately.
    # Both will be disabled if --no-logs is True.
    init_logger(args["--logdir"], args["-v"], args["--no-logs"], args["--quiet"])
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
    args = docopt(__doc__, version="0.3")
    main()
