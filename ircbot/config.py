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
    "freenode": {
        "server": "irc.freenode.net",
        "port": 6667,
        "ssl": False,
        "password": None,
        "identity": identities["demibot"],
        "superadmin": "mikar",
        "admins": [
            "mikar",
            "pld",
        ],
        "channels": [
            "#z1",
            "#z2",
        ]
    },
    "oftc": {
        "server": "irc.oftc.net",
        "port": 6667,
        "ssl": False,
        "password": None,
        "identity": identities["demibot"],
        "admins": [
            "mikar",
            "pld",
        ],
        "channels": [
            "#z1",
            "#z2",
        ]
    },
#     "rizon": {
#         "server": "irc.rizon.net",
#         "port": 6667,
#         "ssl": False,
#         "password": None,
#         "identity": identities["example"],
#         "admins": (
#             "mikar",
#             "pld",
#         ),
#         "channels": (
#             "#z1",
#             "#z2",
#         )
#     },
#     "quakenet": {
#         "server": "irc.quakenet.org",
#         "port": 6667,
#         "ssl": False,
#         "password": None,
#         "identity": identities["example"],
#         "admins": (
#             "mikar",
#             "pld",
#         ),
#         "channels": (
#             "#z1",
#             "#z2",
#         )
#     }
}