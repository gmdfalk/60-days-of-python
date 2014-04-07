from twisted.internet import protocol, reactor
from client import Client
import os
import logging
import sys

log = logging.getLogger("factory")


class Factory(protocol.ClientFactory):

    clients = {}
    moduledir = os.path.join(sys.path[0], "modules/")

    def __init__(self, network_name, network, loglevel):
        self.network_name = network_name
        self.network = network
        self.identity = self.network["identity"]
        self.loglevel = loglevel
        # Namespace for modules
        self.ns = {}
        # Connection retry delays
        self.lost_delay = 10
        self.failed_delay = 30
        init_logging(loglevel)

    def startFactory(self):
        self._loadmodules()
        log.info("Factory started.")

    def clientConnectionLost(self, connector, reason):
        "Reconnect after 10 seconds if the connection to the network is lost"
        log.info("connection lost ({}): reconnecting in {} seconds"
                 .format(reason, self.lost_delay))
        reactor.callLater(self.lost_delay, connector.connect)

    def clientConnectionFailed(self, connector, reason):
        "Reconnect after 30 seconds if the connection to the network fails"
        log.info("connection failed ({}): reconnecting in {} seconds"
                 .format(reason, self.failed_delay))
        reactor.callLater(self.failed_delay, connector.connect)

    def buildProtocol(self, address):
        log.info("Building protocol for {}".format(address))
        p = Client(self)
        self.clients[self.network_name] = p
        return p

    def _finalize_modules(self):
        "Call all module finalizers"
        for module in self._findmodules():
            # If rehashing (module already in namespace),
            # finalize the old instance first.
            if module in self.ns:
                if 'finalize' in self.ns[module][0]:
                    log.info("Finalize - {}".format(module))
                    self.ns[module][0]['finalize']()

    def _loadmodules(self):
        "Load all modules"
        self._finalize_modules()
        for module in self._findmodules():
            env = self._getGlobals()
            log.info("Load module - {}".format(module))
            # Load new version of the module
            execfile(os.path.join(self.moduledir, module), env, env)
            # Initialize module
            if 'init' in env:
                log.info("initialize module - {}".format(module))
                env['init'](self)
            # Add to namespace so we can find it later
            self.ns[module] = (env, env)

    def _unload_removed_modules(self):
        "Unload modules removed from modules -directory"
        # Find all modules in namespace that aren't present in moduledir
        removed_modules = [m for m in self.ns if not m in self._findmodules()]

        for m in removed_modules:
            # finalize module before deleting it
            # TODO: use general _finalize_modules instead of copy-paste
            if 'finalize' in self.ns[m][0]:
                log.info("Finalize - {}".format(m))
                self.ns[m][0]['finalize']()
            del self.ns[m]
            log.info("Removed module - {}".format(m))

    def _findmodules(self):
        "Find all modules"
        modules = [m for m in os.listdir(self.moduledir) if\
                   m.startswith("module_") and m.endswith(".py")]
        return modules

    def _getGlobals(self):
        "Global methods for modules"
        g = {}

        g['get_nick'] = self.get_nick
        g['is_admin'] = self.is_admin
        g['to_utf8'] = self.to_utf8
        g['to_unicode'] = self.to_unicode
        return g

    def get_nick(self, user):
        "Parses nick from nick!user@host"
        return user.split('!', 1)[0]

    def is_admin(self, user):
        "Check if an user has admin privileges."
        if user in self.network["admins"]:
                return True
        return False

    def to_utf8(self, _string):
        "Convert string to UTF-8 if it is unicode"
        if isinstance(_string, unicode):
            _string = _string.encode("UTF-8")
        return _string

    def to_unicode(self, _string):
        "Convert string to UTF-8 if it is unicode"
        if not isinstance(_string, unicode):
            try:
                _string = unicode(_string)
            except:
                try:
                    _string = _string.decode('utf-8')
                except:
                    _string = _string.decode('iso-8859-1')
        return _string


def init_logging(loglevel):
    logger = logging.getLogger()

    levels = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
    logger.setLevel(levels[loglevel])

    default = "%(asctime)-15s %(levelname)-8s %(name)-11s %(message)s"
    formatter = logging.Formatter(default)
    # Append file name + number if debug is enabled

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)