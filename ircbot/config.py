"""config.py

    These connection settings will be used by demibot if started without a
    <server> argument.

    Currently, NickServ and server passwords are read from an "auth" file in
    either the root directory of demibot or ~/.demibot or ~/.config/demibot.
    Alternatively, you obviously can just enter the passwords here in plaintext.
    Other than that, the file should be self-explanatory.

    Tuple for superadmins, sets for admins and channels. Everything else is a
    dict.

    The auth file has a very simple syntax of identifier passphrase, e.g.:
    user nickservpassword
    server serverpassword
"""


def read_authfile(authfile):
    "Reads authentication info from a file"
    auth = {}
    try:
        with open(authfile) as f:
            for line in f:
                name, password = line.split()
                auth[name] = password
    except IOError:
        auth = {}

    return auth

def read_options(use_home):
    "Entry point for main.py to read in the configuration."
    pass

def create_options():
    "Enter your connection settings here."

    superadmins = "pld",  # The comma is important.

    identities = {
        "example": {
            "nickname": "botnick",
            "realname": "",
            "username": "",
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
            "admins":  {"nick3", "nick4"},
            "channels": {"#channel1", "#channel2"},
        },
        "oftc": {
            "server": "irc.oftc.net",
            "port": 6667,
            "ssl": False,
            "password": auth.get("oftc"),
            "identity": identities["example"],
            "superadmins": {"nick1", "nick2"},
            "admins":  {"nick3", "nick4"},
            "channels": {"#channel1", "#channel2"},
        },
    }
