from ConfigParser import SafeConfigParser
from email import parser
from email.Utils import formatdate
from email.mime.text import MIMEText
from getpass import getpass
import logging
import os
import poplib
import smtplib
import sys
import time


log = logging.getLogger("mail")


# See if we can use GnuPG. If not, disable encryption.
use_gnupg = False
try:
    import gnupg
    use_gnupg = True
except ImportError:
    log.error("Could not import gnupg. Encryption disabled.")


class Mail(object):
    pass


class MailHandler(object):

    def __init__(self, account, username, configdir):
        # ConfigParser setup.
        log.debug("Initializing MailHandler with {}, {} in {}."
                  .format(account, username, configdir))
        self.configdir = configdir
        self.configfile = os.path.join(configdir, "gmxmail.ini")
        self.config = SafeConfigParser()

        if not os.path.isfile(self.configfile):
            log.error("Config file not found at {}.".format(self.configfile))
            sys.exit(1)
        self.config.read(self.configfile)

        self.account = account or "emma-stein@gmx.net"
        if not self.config.has_section(self.account) and not username:
            log.error("Got account {} but no username. Exiting."
                      .format(self.account))
            sys.exit()
        self.username = username or self.get_opt("username")
        self.content_subtype = "plain"
        self.content_charset = "utf-8"
        self.user_agent = "gmxmail (https://github.com/mikar/gmxmail"
        # Note: Could also use the config as a dictionary with:
        # self.c = self.config._sections[self.account]
        # But that will someone skip the DEFAULT section so we'll stick with
        # self.get_opt() for now.

    def get_opt(self, option, optiontype=str):
        "Parse an option from config.ini"
        log.debug("Querying option: {}.".format(option))
        section = self.account
        if not self.config.has_section(section):
            section = "DEFAULT"
            log.debug("Section {} not found. Using DEFAULT".format(section))
        if optiontype == int:
            return self.config.getint(section, option)
        elif optiontype == float:
            return self.config.getfloat(section, option)
        elif optiontype == bool:
            return self.config.getboolean(section, option)
        elif optiontype == str:
            return self.config.get(section, option)
        else:
            log.error("Invalid option type: {} ({}).".format(option,
                                                             optiontype))

    def print_options(self):
        "Print all available options. For debugging purposes."
        for i in self.config.options(self.account):
            print i + ":", self.config.get(self.account, i)

    def get_mail(self):
        log.info("Getting mail for {}".format(self.account))

        if not self.username:
            self.username = self.account

        password = getpass("Password for {}: ".format(self.username))
        server = self.get_opt("incserver")
        port = self.get_opt("incport", int)

        # Unnecessarily check if we'll use SSL.
        if self.get_opt("incsecurity") == "SSL":
            session = poplib.POP3_SSL(server, port)
        else:
            session = poplib.POP3(server, port)

        try:
            session.user(self.username)
            session.pass_(password)
        except poplib.error_proto:
            log.error("Authentification failed. Wrong credentials?")
            sys.exit(1)

        messages = [session.retr(i) for i in range(1, len(session.list()[1]))]
        messages = ["\n".join(msg[1]) for msg in messages]
        messages = [parser.Parser().parsestr(msg) for msg in messages]
        for message in messages:
            print message["subject"]
        session.quit()


    def send_mail(self, recipient, header, message, sign, encrypt, key):
        "Sends a mail via SMTP."
        log.info("Sending mail to {} ({}). Sign/Encrypt/AttachKey: {}/{}/{}."
                 .format(recipient, header, sign, encrypt, key))

        recipients = {i for i in recipient.split(",") if "@" in i}
        if not recipients:
            log.error("No valid recipients in {}.".format(recipients))
            return

        # TODO: Hash the password with sha256+salt and only ask once at start-
        # up, if we implement a curse UI.
        if not self.username:
            self.username = self.account
        password = getpass("Password for {}: ".format(self.username))
        server = self.get_opt("outserver")
        port = self.get_opt("outport", int)

        # Split header into CC, BCC and Subject.
        cc, bcc = "", ""
        header = header.split("::")
        if len(header) == 3:
            cc, bcc, subject = header[0], header[1], header[2]
        elif len(header) == 2:
            cc, subject = header[0], header[1]
        else:
            subject = header[0]

        cc = {i for i in cc.split(",") if "@" in i}
        bcc = {i for i in bcc.split(",") if "@" in i}

        # Create the actual header from our gathered information.
        msg = MIMEText(
                       _text=message,
                       _subtype=self.content_subtype,
                       _charset=self.content_charset
                       )
        msg["From"] = self.account
        msg["To"] = ", ".join(recipients)
        if cc:
            msg["Cc"] = ", ".join(cc)
        msg["Date"] = formatdate(time.time())
        msg["User-Agent"] = self.user_agent
        msg["Subject"] = subject

        session = smtplib.SMTP(server, port)
        if logging.getLogger().getEffectiveLevel() > 30:
            session.set_debuglevel(1)

        if self.get_opt("outsecurity"):
            session.ehlo()
            session.starttls()
            session.ehlo()

        # Union of the three sets.
        recipients = recipients | cc | bcc

        session.login(self.username, password)
        session.sendmail(self.account, recipients, msg.as_string())
        log.info("Mail sent from {} to {} ({}).".format(self.account,
                                                        recipients, subject))
        session.quit()
