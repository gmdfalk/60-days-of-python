"""config.py

    This file will be used by demibot if started without commandline arguments.
    Currently, NickServ and server passwords are read from a .auth file in the
    root directory of demibot. This will probably change. Alternatively, you
    obviously can just enter the passwords here in plaintext.
    Other than that, the file should be self-explanatory.
    Tuple for superadmins, sets for admins and channels. Everything else
    is a dict.
"""


def get_auth_info(authfile):
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


auth = get_auth_info(".auth")
# Use a tuple for superadmins and sets for admins & channels.
superadmins = "pld",  # The comma is important.

identities = {
    "demibot": {
        "nickname": "demibot",
        "realname": "the game",
        "username": "demibot",
        "nickserv_pw": auth.get("demibot")
    },
}
networks = {
    "freenode": {
        "server": "irc.freenode.net",
        "port": 6667,
        "ssl": False,
        "password": auth.get("freenode"),
        "identity": identities["demibot"],
        "superadmins": superadmins,
        "admins": set(superadmins) | {"mikar"},  # | is short for set.union().
        "channels": {"#python", "#z1"},
    },
    "oftc": {
        "server": "irc.oftc.net",
        "port": 6667,
        "ssl": False,
        "password": auth.get("oftc"),
        "identity": identities["demibot"],
        "superadmins": superadmins,
        "admins": set(superadmins) | {"mikar"},
        "channels": {"#awesome", "#z1"},
    },
#     "rizon": {
#         "server": "irc.rizon.net",
#         "port": 6667,
#         "ssl": False,
#         "password": auth.get("oftc"),
#         "identity": identities["example"],
#         # It's also possible to list superadmins, admins and channels:
#         "superadmins": (
#             "nick1",
#             "nick2"
#         ),
#         "admins": {
#             "nick1",
#             "nick2",
#         },
#         "channels": {
#             "#z1",
#             "#z2",
#         },
#     },
#     "quakenet": {
#         "server": "irc.quakenet.org",
#         "port": 6667,
#         "ssl": False,
#         "password": auth.get("oftc"),
#         "identity": identities["example"],
#         "superadmins": (
#             "nick1",
#             "nick2"
#         ),
#         "admins": {
#             "nick1",
#             "nick2",
#         },
#         "channels": {
#             "#z1",
#             "#z2",
#         },
#     },
}
