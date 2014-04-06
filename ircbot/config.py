identities = {
    "example": {
        "nickname": "examplebot",
        "realname": "I'm a bot",
        "username": "examplebot",
        "nickserv_pw": None
    },
    "demibot": {
        "nickname": "demibot",
        "realname": "the game",
        "username": "anonymous",
        "nickserv_pw": None
    },
}
networks = {
    "Freenode": {
        "server": "irc.freenode.net",
        "port": 6667,
        "ssl": False,
        "password": None,
        "admins": "mikar",
        "identity": identities["demibot"],
        "channels": (
            "#z1",
            "#z2",
        )
    },
    "OFTC": {
        "server": "irc.oftc.net",
        "port": 6667,
        "ssl": False,
        "password": None,
        "admins": "mikar",
        "identity": identities["demibot"],
        "channels": (
            "#z1",
            "#z2",
        )
    },
#     "Rizon": {
#         "server": "irc.rizon.net",
#         "port": 6667,
#         "ssl": False,
#         "password": None,
#         "admins": "mikar"
#         "identity": identities["example"],
#         "channels": (
#             "#z1",
#             "#z2",
#         )
#     },
#     "Quakenet": {
#         "server": "irc.quakenet.org",
#         "port": 6667,
#         "ssl": False,
#         "password": None,
#         "admins": "mikar"
#         "identity": identities["example"],
#         "channels": (
#             "#z1",
#             "#z2",
#         )
#     }
}