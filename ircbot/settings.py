identities = {
    'myownbot': {
        'nickname': 'myownbot',
        'realname': 'My own bot',
        'username': 'myownbot',
        'nickserv_pw': None
    },
    'maxbot': {
        'nickname': 'maxbot',
        'realname': "anonymous",
        'username': 'the game',
        'nickserv_pw': None
    },
}
networks = {
    'Freenode': {
        'server': 'irc.freenode.net',
        'port': 6667,
        'ssl': False,
        'identity': identities['maxbot'],
        'channels': (
            '#z1',
            '#z2',
        )
    },
    'OFTC': {
        'server': 'irc.oftc.net',
        'port': 6667,
        'ssl': False,
        'identity': identities['maxbot'],
        'channels': (
            '#z1',
            '#z2',
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
#         )
#     }
}