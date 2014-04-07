def get_auth_info(authfile):
    "Reads authentication info from a file"
    auth = {}
    with open(authfile) as f:
        for line in f:
            name, password = line.split()
            auth[name] = password
    return auth

authfile = ".auth"
auth = get_auth_info(authfile)

# Use a tuple for superadmins and sets for admins & channels.
superadmins = ("pld",)  # The comma is important.
channels = {"#z1", "#z2"}

identities = {
    "example": {
        "nickname": "examplebot",
        "realname": "I'm a bot",
        "username": "examplebot",
        "nickserv_pw": auth.get("example")
    },
    "demibot": {
        "nickname": "demibot",
        "realname": "the game",
        "username": "anonymous",
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
        "channels": channels,
    },
    "oftc": {
        "server": "irc.oftc.net",
        "port": 6667,
        "ssl": False,
        "password": auth.get("oftc"),
        "identity": identities["demibot"],
        "superadmins": superadmins,
        "admins": set(superadmins) | {"mikar"},
        "channels": channels,
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
