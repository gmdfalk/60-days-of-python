import ConfigParser
from email import parser
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Utils import formatdate
from getpass import getpass
import logging
import mimetypes
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

    # List of fingerprints of potential recipients. Necessary for encryption.
    FPs = {"MaxDemian": "F0B840E33233E8C33CDA3BF5432B81517FCD8602"}

    def __init__(self, account, username, configdir):
        # ConfigParser setup.
        log.debug("Initializing MailHandler with {}, {} in {}."
                  .format(account, username, configdir))
        self.configdir = configdir
        self.configfile = os.path.join(configdir, "gmxmail.ini")
        self.config = ConfigParser.SafeConfigParser()

        if not os.path.isfile(self.configfile):
            log.error("Config file not found at {}.".format(self.configfile))
            sys.exit(1)
        self.config.read(self.configfile)

        self.account = account or "mikar@gmx.de"
        try:
            self.username = username or self.get_opt("username")
        except ConfigParser.NoOptionError:
            self.username = self.account
            log.debug("No username found. Defaulting to {}."
                      .format(self.account))
        self.content_subtype = "plain"
        self.content_charset = "utf-8"
        self.user_agent = "gmxmail (https://github.com/mikar/gmxmail"
        # Note: Could also use the config as a dictionary with:
        # self.c = self.config._sections[self.account]
        # But that will somehow skip the DEFAULT values so we'll stick with
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
        "Get the mail. Uses poplib as GMX Freemail does not allow imap."
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

        # If the loglevel is DEBUG (10), enable verbose logging.
        if logging.getLogger().getEffectiveLevel() == 10:
            session.set_debuglevel(1)

        try:
            session.user(self.username)
            session.pass_(password)
        except poplib.error_proto:
            log.error("Authentification for {} failed. Wrong credentials?"
                      .format(self.account))
            sys.exit(1)

        messages = [session.retr(i) for i in range(1, len(session.list()[1]))]
        messages = ["\n".join(msg[1]) for msg in messages]
        messages = [parser.Parser().parsestr(msg) for msg in messages]

        # TODO: Make this prettier. Example:
        # http://g33k.wordpress.com/2009/02/04/check-gmail-the-python-way/
        print "You have {} new messages.".format(len(messages))
        for m in messages:
            print "{}, [{}], ({})".format(m["From"], m["Subject"], m["Date"])
        session.quit()


    def send_mail(self, recipient, header, message,
                  sign, encrypt, attachkey, dryrun):
        "Sends a mail via SMTP."
        log.info("Sending mail to {} ({}). Sign/Encrypt/AttachKey: {}/{}/{}."
                 .format(recipient, header, sign, encrypt, attachkey))

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

        # Initialize our message to attach signatures/keyfiles, body etc to.
        msg = MIMEMultipart()

        if sign or encrypt:
            gpg = gnupg.GPG()
            privkeyid = self.get_opt("privatekeyid")
            privkeyfp = self.get_opt("privatekeyfp")
            for i in gpg.list_keys():
                if "432B81517FCD8602" in i["keyid"]:
                     break
            else:
                log.error("{} not found in gpg.list_keys().".format(privkeyid))
                sys.exit(1)
            if sign and encrypt:
                encrypted = str(gpg.encrypt(message, self.FPs["MaxDemian"],
                                            sign=privkeyfp))
                if encrypted:
                    encryptedtext = MIMEText(
                                           _text=encrypted,
                                           _subtype=self.content_subtype,
                                           _charset=self.content_charset
                                           )
                    msg.attach(encryptedtext)
                else:
                    log.error("Failed to encrypt the message.")
                    sys.exit(1)
            elif sign:
#                 message = msg.as_string().replace('\n', '\r\n')
                signed = str(gpg.sign(message, keyid=privkeyid))
                if signed:
                    signedtext = MIMEText(
                                       _text=signed,
                                       _subtype=self.content_subtype,
                                       _charset=self.content_charset
                                       )
                    msg.attach(signedtext)
                else:
                    log.error("Failed to sign the message.")
                    sys.exit(1)

            elif encrypt:
                encrypted = str(gpg.encrypt(message, self.FPs["MaxDemian"]))
                if encrypted:
                    encryptedtext = MIMEText(
                                           _text=encrypted,
                                           _subtype=self.content_subtype,
                                           _charset=self.content_charset
                                           )
                    msg.attach(encryptedtext)
                else:
                    log.error("Failed to encrypt the message.")
                    sys.exit(1)
            else:
                log.error("No GPG keys found.")

        pubkeyloc = None
        if attachkey:  # Attach GPG Public attachkey.
            pubkeyfile = self.get_opt("publickeyfile")
            if os.path.isfile(pubkeyfile):
                pubkeyloc = pubkeyfile
            elif os.path.isfile(os.path.join(self.configdir, pubkeyfile)):
                pubkeyloc = os.path.join(self.configdir, pubkeyfile)
            else:
                log.error("Public attachkey '{}' could not be found."
                          .format(pubkeyfile))
        if pubkeyloc:
            ctype, encoding = mimetypes.guess_type(pubkeyloc)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            if maintype == 'text':
                with open(pubkeyloc) as f:
#                     keyatt = f.read()
                    keyatt = MIMEText(
                                      f.read(),
                                      _subtype=subtype,
                                      _charset=self.content_charset)
                keyatt.add_header(
                        'Content-Disposition',
                        'attachment',
                        filename=pubkeyfile
                )
                msg.attach(keyatt)
                log.info("Attached public attachkey {} to message."
                         .format(pubkeyfile))
            else:
                log.error("{} is not a textfile. Sure it's a GPG Key?"
                          .format(pubkeyloc))

        # Add Mime infos to the message.
        msg["From"] = self.account
        msg["To"] = ", ".join(recipients)
        if cc:
            msg["Cc"] = ", ".join(cc)
        msg["Date"] = formatdate(time.time())
        msg["User-Agent"] = self.user_agent
        msg["Subject"] = subject

        # If --dryrun is enabled, we exit here.
        if dryrun:
            print msg
            sys.exit()
        session = smtplib.SMTP(server, port)
        # If the loglevel is DEBUG (10), enable verbose logging.
#         if logging.getLogger().getEffectiveLevel() == 10:
#             session.set_debuglevel(1)

        if self.get_opt("outsecurity"):
            session.ehlo()
            session.starttls()
            session.ehlo()

        # Union of the three sets.
        recipients = recipients | cc | bcc

        try:
            session.login(self.username, password)
        except smtplib.SMTPAuthenticationError:
            log.error("Authentication failed. Wrong credentials?")
            sys.exit(1)

        # TODO: Add footer (with user-agent, timestamp?)
        session.sendmail(self.account, recipients, msg.as_string())
        log.info("Mail sent from {} to {} ({}).".format(self.account,
                                                        recipients, subject))
        session.quit()
