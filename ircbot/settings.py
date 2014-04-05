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
        'server': 'irc.freenode.net',
        'port': 6667,
        'ssl': False,
        'identity': identity['myownbot'],
        'channels': (
            '#z1',
            '#z2',
            '#z3',
        )
    },
    'OFTC': {
        'server': 'irc.oftc.net',
        'port': 6667,
        'ssl': False,
        'identity': identity['myownbot'],
        'channels': (
            '#z1',
            '#z2',
            '#z3',
        )
    },
#     'Rizon': {
#         'server': 'irc.rizon.net',
#         'port': 6667,
#         'ssl': False,
#         'identity': identity['myownbot'],
#         'channels': (
#             '#z1',
#             '#z2',
#             '#z3',
#         )
#     },
#     'Quakenet': {
#         'server': 'irc.quakenet.org',
#         'port': 6667,
#         'ssl': False,
#         'identity': identity['myownbot'],
#         'channels': (
#             '#z1',
#             '#z2',
#             '#z3',
#         )
#     }
}