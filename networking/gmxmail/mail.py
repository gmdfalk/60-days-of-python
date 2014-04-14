from ConfigParser import SafeConfigParser
import logging
import smtplib


log = logging.getLogger("mail")


class Mail(object):
    pass


class MailHandler(object):

    def __init__(self, account, username, password):
        # ConfigParser setup.
        self.config = SafeConfigParser()
        self.config.read("config.ini")

        # Read in the options.
        self.account = account or "emma-stein@gmx.net"
        self.username = username or self.get_opt("username")
        self.password = password or self.decode_pass(self.get_opt("password"))

    def decode_pass(self, password):
        pass

    def get_opt(self, option):
        log.debug("Querying option: {}.".format(option))
        return self.config.get(self.account, option)

    def print_options(self):
        for i in self.config.options(self.account):
            print i + ":", self.config.get(self.account, i)

    def get_mail(self):
        log.info("Getting mail.")


    def send_mail(self, recipients, message, sign, encrypt, attach):
        log.info("Sending mail.")

        recipients = {i for i in recipients.split(",") if "@" in i}
        if not recipients:
            log.error("No valid recipients in {}.".format(recipients))
            return

        session = smtplib.SMTP(self.get_opt("outserver"))
        session.login(self.user, self.password)
        session.sendmail(self.account, recipients, message)


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
