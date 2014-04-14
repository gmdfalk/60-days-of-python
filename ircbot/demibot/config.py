"""config.py

    These connection settings will be used by demibot if started without a
    <server> argument.

    Currently, NickServ and server passwords are read from an "auth" file in
    either the root directory of demibot or ~/.demibot or ~/.config/demibot.
    Alternatively, you obviously can just enter the passwords here in plaintext.
    Other than that, the file should be self-explanatory.

    Sets for admins and channels. Everything else is a dict.

    The auth file has a very simple syntax of identifier passphrase, e.g.:
    user nickservpassword
    server serverpassword
"""
import os


def read_authfile(configdir):
    "Reads authentication info from a file"
    auth = {}
    try:
        authfile = os.path.join(configdir, "auth")
        with open(authfile) as f:
            for line in f:
                name, password = line.split()
                auth[name] = password
    except IOError as e:
        print "IOError: {}.\nCould not read authentication file.".format(e)
        auth = {}
    return auth


def create_options(configdir):
    "Enter your the network and identity settings here."

    # Read authentication information from a file into a dict to "get" from.
    auth = read_authfile(configdir)

    identities = {
        "example": {
            "nickname": "botnick",
            "realname": "botnick",
            "username": "botnick",
            "nickserv_pw": auth.get("botnick")
        },
    }
    networks = {
        "freenode": {
            "server": "irc.freenode.net",
            "port": 6667,
            "ssl": False,
            "password": auth.get("freenode"),
            "identity": identities["example"],
            "superadmins": {"nick1", "nick2"},
            "admins":  {},
            "channels": {"#channel1", "#channel2"},
        },
        "oftc": {
            "server": "irc.oftc.net",
            "port": 6667,
            "ssl": False,
            "password": auth.get("oftc"),
            "identity": identities["example"],
            "superadmins": {"nick1", "nick2"},
            "admins":  {},
            "channels": {"#channel1", "#channel2"},
        },
    }

    return networks
