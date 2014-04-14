from ConfigParser import SafeConfigParser
import logging
import smtplib


log = logging.getLogger("mail")


class Mail(object):
    pass


class MailHandler(object):

    def __init__(self, account, username, password):
        # ConfigParser setup.
        self.c = SafeConfigParser()
        self.c.read("config.ini")

        # Read in the options.
        self.account = account or "emma-stein@gmx.net"
        for i in self.c.options(self.account):
            print self.i, self.c.get(self.account, i)

        print self.i
#         self.username = username or self.get_option("username")
#         self.password = password or self.get_option("password")
#         self.inc_security = self.get_option("incomingsecurity")
#         self.inc_server = self.get_option("incomingserver")
#         self.inc_port = self.get_option("incomingport")
#         self.out_security = self.get_option("outgoingsecurity")
#         self.out_server = self.get_option("outgoingserver")
#         self.out_port = self.get_option("outgoingport")
#         self.autofetch = self.get_option("autofetch")
#         self.autofetchinterval = self.get_option("autofetchinterval")
#         self.deleteafterfetch = self.get_option("deleteafterfetch")
#         self.publickey = self.get_option("publickey")

    def get_option(self, option):
        return self.c.get(self.account, option)

    def get_mail(self):
        log.info("Getting mail.")
#         self.print_options()

    def send_mail(self, recipients, message, sign, encrypt, attach):
        log.info("Sending mail.")

        parser = SafeConfigParser()
        log.info("Parsing configuration file.")
        parser.read("config.ini")

#     server = 'mail.server.com'
#     user = ''
#     password = ''
#
#     recipients = ['user@mail.com', 'other@mail.com']
#     sender = 'you@mail.com'
#     message = 'Hello World'
#
#     session = smtplib.SMTP(server)
#     # if your SMTP server doesn't need authentications,
#     # you don't need the following line:
#     session.login(user, password)
#     session.sendmail(sender, recipients, message)


def parse_config():
    parser = SafeConfigParser()
    log.info("Parsing configuration file.")
    parser.read("config.ini")

    # Get one option.
    print parser.get("DEFAULT", "autofetch")

    # Get all sections and their options.
    for section_name in parser.sections():
        print 'Section:', section_name
        print 'Options:', parser.options(section_name)
        for name, value in parser.items(section_name):
            print '  %s = %s' % (name, value)
        print

    # See if sections exist:
    for section in ['wiki', 'emma', 'dvcs' ]:
        print '%-19s: %s' % (section, parser.has_section(section))
        for option in [ 'username', 'password', 'url', 'description' ]:
                print '%s.%-12s  : %s' % (section, option,
                                          parser.has_option(section, option))
    print parser.getint("emma", "outgoingport")
    print parser.getboolean("emma", "autofetch")
