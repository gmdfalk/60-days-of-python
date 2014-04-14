from ConfigParser import SafeConfigParser
import logging
import smtplib
from getpass import getpass


log = logging.getLogger("mail")


class Mail(object):
    pass


class MailHandler(object):

    def __init__(self, account, username):
        # ConfigParser setup.
        self.config = SafeConfigParser()
        self.config.read("config.ini")
        self.account = account or "emma-stein@gmx.net"
        self.username = username or self.get_opt("username")
        self.use_tls = True

    def get_opt(self, option):
        "Parse an option from config.ini"
        log.debug("Querying option: {}.".format(option))
        section = self.account
        if not self.config.has_section(section):
            section = "DEFAULT"
        return self.config.get(section, option)


    def print_options(self):
        "Print all available options. For debugging purposes."
        for i in self.config.options(self.account):
            print i + ":", self.config.get(self.account, i)


    def get_mail(self):
        log.info("Getting mail.")


    def send_mail(self, recipients, message, sign, encrypt, attach):
        log.info("Sending mail.")
        recipients = [i for i in recipients.split(",") if "@" in i]
        if not recipients:
            log.error("No valid recipients in {}.".format(recipients))
            return

        password = getpass("Password for {}: ".format(self.username))
        server = self.get_opt("outserver")
        port = self.config.getint(self.account, "outport")

        smtp = smtplib.SMTP()
        smtp.connect(server, port)

        if self.use_tls:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

        if not self.username:
            self.username = self.account

        smtp.login(self.username, password)
        smtp.sendmail(self.account, recipients, message)
        smtp.close()


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
