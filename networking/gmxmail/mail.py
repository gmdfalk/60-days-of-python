from ConfigParser import SafeConfigParser
import logging
import smtplib


log = logging.getLogger("mail")


class Mail(object):
    pass


class MailHandler(object):

    def __init__(self, account, password, ssl):
        parser = SafeConfigParser()
        if account:
            self.account = account
        if password:
            self.password = password
        if ssl:
            self.ssl = ssl


    def get_mail(self, recipients, message, sign, encrypt, attach):
        log.info("Getting mail.")

    def send_mail(self, recipients, message, sign, encrypt, attach, account):
        log.info("Sending mail.")

        parser = SafeConfigParser()
        log.info("Parsing configuration file.")
        parser.read("config.ini")

        if parser.has_section(account):
            print '%-19s: %s' % (account, parser.has_section(account))
            for option in ["username", "password"]:
                    print '%s.%-12s  : %s' % (account, option,
                                              parser.has_option(account, option))
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
