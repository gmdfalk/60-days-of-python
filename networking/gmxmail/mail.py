from ConfigParser import SafeConfigParser
from email.Header import Header
from email.Utils import formatdate
from email.mime.text import MIMEText
from getpass import getpass
import logging
import os
import smtplib
import time
import sys


log = logging.getLogger("mail")


class Mail(object):
    pass


class MailHandler(object):

    def __init__(self, account, username, configdir):
        # ConfigParser setup.
        self.configdir = configdir
        self.configfile = os.path.join(configdir, "gmxmail.ini")
        self.config = SafeConfigParser()
        if not os.path.isfile(self.configfile):
            log.error("Config file not found at {}.".format(self.configfile))
            sys.exit(1)
        self.config.read(self.configfile)
        self.account = account or "emma-stein@gmx.net"
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
        if optiontype == int:
            return self.config.getint(self.account, option)
        elif optiontype == float:
            return self.config.getfloat(self.account, option)
        elif optiontype == bool:
            return self.config.getboolean(self.account, option)
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
        log.info("Getting mail.")


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
        header = header.split("::")
        if len(header) == 3:
            cc, bcc, subject = header[0], header[1], header[2]
        elif len(header) == 2:
            cc, bcc, subject = header[0], set(), header[1]
        else:
            cc, bcc, subject = set(), set(), header[0]

        if cc and not "@" in cc:
            log.warn("Invalid CC: {}".format(cc))
            cc = set()
        elif "," in cc:
            cc = {i for i in cc.split(",") if "@" in i}
        if bcc and not "@" in bcc:
            log.warn("Invalid BCC: {}".format(bcc))
            bcc = set()
        elif "," in bcc:
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
        session.quit()
