identity = {
    'myownbot': {
        'nickname': 'myownbot',
        'realname': 'My own bot',
        'username': 'myownbot',
        'nickserv_pw': None
    },
    'maxbot': {
        'nickname': 'maxbot',
        'realname': "Max' bot",
        'username': 'maxbot',
        'nickserv_pw': None
    },
}
networks = {
    'Freenode': {
        'host': 'irc.freenode.net',
        'port': 6667,
        'ssl': False,
        'identity': identity['myownbot'],
        'autojoin': (
            '#z1',
            '#z2',
            '#z3',
        )
    },
    'OFTC': {
        'host': 'irc.oftc.net',
        'port': 6667,
        'ssl': False,
        'identity': identity['myownbot'],
        'autojoin': (
            '#z1',
            '#z2',
            '#z3',
        )
    },
#     'Rizon': {
#         'host': 'irc.rizon.net',
#         'port': 6667,
#         'ssl': False,
#         'identity': identity['myownbot'],
#         'autojoin': (
#             '#z1',
#             '#z2',
#             '#z3',
#         )
#     },
#     'Quakenet': {
#         'host': 'irc.quakenet.org',
#         'port': 6667,
#         'ssl': False,
#         'identity': identity['myownbot'],
#         'autojoin': (
#             '#z1',
#             '#z2',
#             '#z3',
#         )
#     }
}