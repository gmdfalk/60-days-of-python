# encoding: utf-8
# TODO: Exclude option
# TODO: Fix count (~i)
import fnmatch
import logging
import os
import re
import sys
from unicodedata import normalize, category
from copy import deepcopy


log = logging.getLogger("fileops")


def configure_logger(loglevel=2, quiet=False):
    "Creates the logger instance and adds handlers and formatting."
    logger = logging.getLogger()

    # Set the loglevel.
    if loglevel > 3:
        loglevel = 3  # Cap at 3 to avoid index errors.
    levels = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
    logger.setLevel(levels[loglevel])

    logformat = "%(asctime)-14s %(levelname)-8s %(name)-8s %(message)s"

    formatter = logging.Formatter(logformat, "%Y-%m-%d %H:%M:%S")

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if quiet:
        log.info("Quiet mode: logging disabled.")
        logging.disable(logging.ERROR)


class FileOps(object):

    def __init__(self, quiet=False, verbosity=1,
                 dirsonly=False, filesonly=False, recursive=False,
                 hidden=False, simulate=False, interactive=False, prompt=False,
                 noclobber=False, keepext=False, regex=False, exclude=None,
                 media=False, accents=False, lower=False, upper=False,
                 remdups=False, remext=False, remnonwords=False,
                 ignorecase=False, countpos=0):
        # List of available options.
        self.opts = ("quiet", "verbosity",
                     "dirsonly", "filesonly", "recursive", "hidden",
                     "simulate", "interactive", "prompt", "noclobber",
                     "keepext", "regex", "exclude", "media", "accents",
                     "lower", "upper", "remdups", "remext", "remnonwords",
                     "ignorecase", "countpos",
                     "autostop", "mirror", "spacecheck", "spacemode",
                     "capitalizecheck", "capitalizemode",
                     "insertcheck", "insertpos", "insertedit",
                     "countcheck", "countfill", "countbase", "countpreedit",
                     "countsufedit", "varcheck",
                     "deletecheck", "deletestart", "deleteend",
                     "replacecheck")
        # Universal options:
        self._dirsonly = dirsonly  # Only edit directory names.
        self._filesonly = False if dirsonly else filesonly  # Only file names.
        self._recursive = recursive  # Look for files recursively
        self._hidden = hidden  # Look at hidden files and directories, too.
        self._simulate = simulate  # Simulate renaming and dump result to stdout.
        self._interactive = interactive  # Confirm before overwriting.
        self._prompt = prompt  # Confirm all rename actions.
        self._noclobber = noclobber  # Don't overwrite anything.
        self._keepext = keepext  # Don't modify remext.
        self._countpos = countpos  # Adds numerical index at position.
        self._regex = regex  # Use regular expressions instead of glob/fnmatch.
        self._exclude = exclude  # List of strings to exclude from targets.
        self._accents = accents  # Normalize accents (ñé becomes ne).
        self._lower = lower  # Convert target to lowercase.
        self._upper = upper  # Convert target to uppercase.
        self._ignorecase = ignorecase  # Case sensitivity.
        self._media = media  # Mode to sanitize NTFS-filenames/dirnames.
        self._remdups = remdups  # Remove remdups.
        self._remnonwords = remnonwords  # Only allow wordchars (\w)
        self._remext = remext  # Remove all remext.
        # Initialize GUI options.
        self._autostop = False  # Automatically stop execution on rename error.
        self._mirror = False  # Mirror manual rename to all targets.
        self._capitalizecheck = False  # Whether to apply the capitalizemode.
        self._capitalizemode = 0  # 0=lc, 1=uc, 2=flfw, 3=flew
        self._spacecheck = False  # Whether to apply the spacemode.
        self._spacemode = 0  # 0=su, 1=sh, 2=sd, 3=ds, 4=hs, 5=us
        self._countcheck = False  # Whether to add a counter to the targets.
        self._countbase = 1  # Base to start counting from.
        self._countstep = 1
        self._countfill = True  # 9->10: 9 becomes 09. 99->100: 99 becomes 099.
        self._countpreedit = ""  # String that is prepended to the counter.
        self._countsufedit = ""  # String that is appended to the counter.
        self._insertcheck = False  # Whether to apply an insertion.
        self._insertpos = 0  # Position/Index to insert at.
        self._insertedit = ""  # The inserted text/string.
        self._deletecheck = False  # Whether to delete a specified range.
        self._deletestart = 0  # Start index of deletion sequence.
        self._deleteend = 1  # End index of deletion sequence.
        self._replacecheck = True  # Whether to apply source/target patterns.
        self._matchonly = False
        self._removecheck = False
        self._varcheck = False  # Whether to apply various options (accents).

        # Create the logger.
        configure_logger(verbosity, quiet)
        self.history = []  # History of commited operations, useful to undo.
        self.defaultopts = {i:getattr(self, "_" + i, None) for i in self.opts}

    def get_options(self, *args):
        if args:
            return {i: getattr(self, i, None) for i in args}
        return {i: getattr(self, i, None) for i in self.opts}

    def set_options(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def restore_options(self):
        self.set_options(**self.defaultopts)

    def stage(self, path=None, srcpat=None, destpat=None):
        """Initialize the rename operation. Returns list of targets and their
        preview."""
        self.replacecheck = False
        if not path:
            path = os.getcwd()
        if srcpat is None:
            srcpat = "*"
        if destpat is None:
            destpat = "*"
        if self.media:
            self.spacecheck = True
            self.spacemode = 0
            self.capitalizecheck = True
            self.capitalizemode = 0
            self.removecheck = True
            self.remdups = True
            self.keepext = True

        targets = self.find_targets(path, srcpat)
        joinedtargets = self.joinext(targets)
        previews = self.modify_targets(deepcopy(joinedtargets), srcpat, destpat)
        print "t:", targets
        print "p:", previews
        log.debug(targets == previews)
        return targets, previews
#         matches = self.match_targets(targets, expression)
#         print matches
        # [i for i, j in zip(a, b) if i != j]

    def commit(self, targets):
        if self.simulate:
            print "{} to {}".format(targets[1], targets[2])
        # clean up self.exclude

    def undo(self, action):
        pass

    def joinext(self, targets):
        """Joins a list of targets into [root, name+ ext] per item."""
        if self.keepext:
            return targets

        joinedtargets = []
        for i in targets:
            if len(i) > 2 and not self.remext:
                i = [i[0], i[1] + i[2]]
            else:
                i = [i[0], i[1]]
            joinedtargets.append(i)

        return joinedtargets

    def match_files(self, srcpat, files, root):
        """Splits a list of files into filename and extension."""
        target = []
        for f in files:
            if self.match(srcpat, f):
#                 if self.keepext:
                fname, ext = os.path.splitext(f)
                target.append([root, fname, ext])
#                 else:
#                     target.append([root, f])
        return target

    def match(self, srcpat, target):
        """Searches target for pattern and returns a bool."""
        if self.regex:
            if re.search(srcpat, target):
                return True
        else:
            if fnmatch.fnmatch(target, srcpat):
                return True
        return False

    def find_targets(self, path, srcpat):
        """Creates a list of files and/or directories to work with."""
        targets = []
        for root, dirs, files in os.walk(path):
            root += "/"
            root = unicode(root, "utf-8")
            dirs = sorted([unicode(d, "utf-8") for d in dirs])
            files = sorted([unicode(f, "utf-8") for f in files])
            # Check the found files and dirs against our regex/glob filter.
            if self.dirsonly:
                target = [[root, d] for d in dirs if self.match(srcpat, d)]
            elif self.filesonly:
                target = self.match_files(srcpat, files, root)
            else:
                target = [[root, d] for d in dirs if self.match(srcpat, d)]
                target += self.match_files(srcpat, files, root)

            # Exclude hidden and explicitly excluded files+dirs.
            if self.hidden:
                targets.extend(target)
            else:
                targets.extend(i for i in target if not i[1].startswith("."))
            # TODO: Implement this correctly (regex/glob?).
            if self.exclude:
                targets = [i for i in targets if i not in self.exclude]

            # Do not enter the second loop for non-recursive searches.
            if not self.recursive:
                break
        return targets

    def modify_targets(self, previews, srcpat, destpat):
        # TODO: Handle case sensitivity (re.IGNORECASE)
        if self.countcheck:
            countlen = len(str(len(previews)))
            countrange = range(self.countbase, len(previews) + 1, self.countstep)
            if self.countfill:
                count = (str(i).rjust(countlen, "0") for i in countrange)
            else:
                count = (str(i) for i in countrange)

        for preview in previews:
            name = preview[1]
            print name
            if self.replacecheck:
                name = self.apply_replace(name, srcpat, destpat)
            if self.capitalizecheck:
                name = self.apply_capitalize(name)
            if self.spacecheck:
                name = self.apply_space(name)
            if self.countcheck:
                try:
                    name = self.apply_count(name, count.next())
                except StopIteration:
                    pass
            if self.deletecheck:
                name = self.apply_delete(name)
            if self.removecheck:
                name = self.apply_remove(name)
            if self.insertcheck:
                name = self.apply_insert(name)

            preview[1] = name

        return previews

    def apply_space(self, s):
        if not self.spacecheck:
            return s

        if self.spacemode == 0:
            s = s.replace(" ", "_")
        elif self.spacemode == 1:
            s = s.replace(" ", "-")
        elif self.spacemode == 2:
            s = s.replace(" ", ".")
        elif self.spacemode == 3:
            s = s.replace(".", " ")
        elif self.spacemode == 4:
            s = s.replace("-", " ")
        elif self.spacemode == 5:
            s = s.replace("_", " ")

        return s
#         self._interactive = interactive  # Confirm before overwriting.
#         self._exclude = exclude  # List of strings to exclude from targets.
#         self._ignorecase = ignorecase  # Case sensitivity.
#         self._remext = remext  # Remove all remext.

    def apply_capitalize(self, s):
        if not self.capitalizecheck:
            return s

        if self.capitalizemode == 0:
            s = s.lower()
        elif self.capitalizemode == 1:
            s = s.upper()
        elif self.capitalizemode == 2:
            s = s.capitalize()
        elif self.capitalizemode == 3:
            # news = s.title()
            s = " ".join([c.capitalize() for c in s.split()])

        return s

    def apply_insert(self, s):
        if not self.insertcheck or not self.insertedit:
            return s
        s = list(s)
        s.insert(self.insertpos, self.insertedit)
        return "".join(s)

    def apply_count(self, s, count):
        if not self.countcheck:
            return s
        s = list(s)

        if self.countpreedit:
            count = self.countpreedit + count
        if self.countsufedit:
            count += self.countsufedit
        s.insert(self.countpos, count)

        return "".join(s)

    def apply_delete(self, s):
        if not self.deletecheck:
            return s
        return s[:self.deletestart] + s[self.deleteend:]

    def apply_remove(self, s):
        if not self.removecheck:
            return s
        if self.remdups:
            s = re.sub(r"([-_ .])\1+", r"\1", s)
        if self.remnonwords:
            s = re.sub("\W", "", s)
        return s

    def apply_replace(self, s, srcpat, destpat):
        if not self.replacecheck:
            return s
        # Translate glob to regular expression.
        if not self.regex:
            srcpat = fnmatch.translate(srcpat)
            destpat = fnmatch.translate(destpat)
        srcmatch = re.search(srcpat, s)
        if srcmatch:
            log.debug("found src: {}.".format(srcmatch.group()))
        destmatch = re.search(destpat, s)
        if destmatch:
            log.debug("found dest: {}.".format(destmatch.group()))
        log.debug("{}, {}, {}, {}".format(srcpat, destpat, srcmatch, destmatch))

        # TODO: Two functions: one to convert a glob into a pattern
        # and another to convert one into a replacement.
        return s

    def apply_various(self, s):
        if not self.varcheck:
            return
        if self.accents:
            s = "".join(c for c in normalize("NFD", s) if category(c) != "Mn")
        return s

    @property
    def dirsonly(self):
        return self._dirsonly

    @dirsonly.setter
    def dirsonly(self, boolean):
        log.debug("dirsonly: {}".format(boolean))
        self._dirsonly = boolean
        if self.dirsonly:
            self.filesonly = False

    @property
    def filesonly(self):
        return self._filesonly

    @filesonly.setter
    def filesonly(self, boolean):
        log.debug("filesonly: {}".format(boolean))
        self._filesonly = boolean
        if self.filesonly:
            self.dirsonly = False

    @property
    def recursive(self):
        return self._recursive

    @recursive.setter
    def recursive(self, boolean):
        log.debug("recursive: {}".format(boolean))
        self._recursive = boolean

    @property
    def hidden(self):
        return self._hidden

    @hidden.setter
    def hidden(self, boolean):
        log.debug("hidden: {}".format(boolean))
        self._hidden = boolean

    @property
    def simulate(self):
        return self._simulate

    @simulate.setter
    def simulate(self, boolean):
        log.debug("simulate: {}".format(boolean))
        self._simulate = boolean

    @property
    def interactive(self):
        return self._interactive

    @interactive.setter
    def interactive(self, boolean):
        log.debug("interactive: {}".format(boolean))
        self._interactive = boolean

    @property
    def prompt(self):
        return self._prompt

    @prompt.setter
    def prompt(self, boolean):
        log.debug("simulate: {}".format(boolean))
        self._prompt = boolean

    @property
    def noclobber(self):
        return self._noclobber

    @noclobber.setter
    def noclobber(self, boolean):
        log.debug("noclobber: {}".format(boolean))
        self._noclobber = boolean

    @property
    def keepext(self):
        return self._keepext

    @keepext.setter
    def keepext(self, boolean):
        log.debug("keepext: {}.".format(boolean))
        self._keepext = boolean

    @property
    def regex(self):
        return self._regex

    @regex.setter
    def regex(self, boolean):
        log.debug("regex: {}.".format(boolean))
        self._regex = boolean

    @property
    def varcheck(self):
        return self._varcheck

    @varcheck.setter
    def varcheck(self, boolean):
        log.debug("varcheck: {}".format(boolean))
        self._varcheck = boolean

    @property
    def accents(self):
        return self._accents

    @accents.setter
    def accents(self, boolean):
        log.debug("accents: {}".format(boolean))
        self._accents = boolean

    @property
    def exclude(self):
        return self._exclude

    @exclude.setter
    def exclude(self, names):
        log.debug("Excluding {}.".format(names))
        self._exclude = names

    @property
    def autostop(self):
        return self._autostop

    @autostop.setter
    def autostop(self, boolean):
        log.debug("autostop: {}".format(boolean))
        self._autostop = boolean

    @property
    def mirror(self):
        return self._mirror

    @mirror.setter
    def mirror(self, boolean):
        log.debug("mirror: {}".format(boolean))
        self._mirror = boolean

    @property
    def removecheck(self):
        return self._removecheck

    @removecheck.setter
    def removecheck(self, boolean):
        log.debug("removecheck: {}".format(boolean))
        self._removecheck = boolean

    @property
    def remnonwords(self):
        return self._remnonwords

    @remnonwords.setter
    def remnonwords(self, boolean):
        log.debug("remnonwords: {}".format(boolean))
        self._remnonwords = boolean

    @property
    def remext(self):
        return self._remext

    @remext.setter
    def remext(self, boolean):
        log.debug("remext: {}".format(boolean))
        self._remext = boolean

    @property
    def remdups(self):
        return self._remdups

    @remdups.setter
    def remdups(self, boolean):
        log.debug("remdups: {}".format(boolean))
        self._remdups = boolean

    @property
    def lower(self):
        return self._lower

    @lower.setter
    def lower(self, boolean):
        log.debug("lower: {}".format(boolean))
        self._lower = boolean

    @property
    def upper(self):
        return self._upper

    @upper.setter
    def upper(self, boolean):
        log.debug("upper: {}".format(boolean))
        self._upper = boolean

    @property
    def ignorecase(self):
        return self._ignorecase

    @ignorecase.setter
    def ignorecase(self, boolean):
        log.debug("ignorecase: {}".format(boolean))
        self._ignorecase = boolean

    @property
    def nowords(self):
        return self._nowords

    @nowords.setter
    def nowords(self, boolean):
        log.debug("nowords: {}".format(boolean))
        self._nowords = boolean

    @property
    def media(self):
        return self._media

    @media.setter
    def media(self, boolean):
        log.debug("media: {}".format(boolean))
        self._media = boolean

    @property
    def countcheck(self):
        return self._countcheck

    @countcheck.setter
    def countcheck(self, boolean):
        log.debug("countcheck: {}".format(boolean))
        self._countcheck = boolean

    @property
    def countfill(self):
        return self._countfill

    @countfill.setter
    def countfill(self, boolean):
        log.debug("countfill: {}".format(boolean))
        self._countfill = boolean

    @property
    def countpos(self):
        return self._countpos

    @countpos.setter
    def countpos(self, index):
        log.debug("countpos: {}".format(index))
        self._countpos = index

    @property
    def countbase(self):
        return self._countbase

    @countbase.setter
    def countbase(self, num):
        log.debug("countbase: {}".format(num))
        self._countbase = num

    @property
    def countstep(self):
        return self._countstep

    @countstep.setter
    def countstep(self, num):
        log.debug("countstep: {}".format(num))
        self._countstep = num

    @property
    def countpreedit(self):
        return self._countpreedit

    @countpreedit.setter
    def countpreedit(self, text):
        log.debug("countpreedit: {}".format(text))
        self._countpreedit = text

    @property
    def countsufedit(self):
        return self._countsufedit

    @countsufedit.setter
    def countsufedit(self, text):
        log.debug("countsufedit: {}".format(text))
        self._countsufedit = text

    @property
    def insertcheck(self):
        return self._insertcheck

    @insertcheck.setter
    def insertcheck(self, boolean):
        log.debug("insertcheck: {}".format(boolean))
        self._insertcheck = boolean

    @property
    def insertpos(self):
        return self._insertpos

    @insertpos.setter
    def insertpos(self, index):
        log.debug("insertpos: {}".format(index))
        self._insertpos = index

    @property
    def insertedit(self):
        return self._insertedit

    @insertedit.setter
    def insertedit(self, text):
        log.debug("insertedit: {}.".format(text))
        self._insertedit = text

    @property
    def deletecheck(self):
        return self._deletecheck

    @deletecheck.setter
    def deletecheck(self, boolean):
        log.debug("deletecheck: {}".format(boolean))
        self._deletecheck = boolean

    @property
    def deletestart(self):
        return self._deletestart

    @deletestart.setter
    def deletestart(self, index):
        log.debug("deletestart: {}".format(index))
        self._deletestart = index

    @property
    def deleteend(self):
        return self._deleteend

    @deleteend.setter
    def deleteend(self, index):
        log.debug("deleteend: {}".format(index))
        self._deleteend = index

    @property
    def replacecheck(self):
        return self._replacecheck

    @replacecheck.setter
    def replacecheck(self, boolean):
        log.debug("replacecheck: {}".format(boolean))
        self._replacecheck = boolean

    @property
    def capitalizecheck(self):
        return self._capitalizecheck

    @capitalizecheck.setter
    def capitalizecheck(self, boolean):
        log.debug("capitalizecheck: {}".format(boolean))
        self._capitalizecheck = boolean

    @property
    def capitalizemode(self):
        return self._capitalizemode

    @capitalizemode.setter
    def capitalizemode(self, num):
        log.debug("capitalizemode: {}".format(num))
        self._capitalizemode = num

    @property
    def spacecheck(self):
        return self._spacecheck

    @spacecheck.setter
    def spacecheck(self, boolean):
        log.debug("spacecheck: {}".format(boolean))
        self._spacecheck = boolean

    @property
    def spacemode(self):
        return self._spacemode

    @spacemode.setter
    def spacemode(self, num):
        log.debug("spacemode: {}".format(num))
        self._spacemode = num


if __name__ == "__main__":
    fileops = FileOps(hidden=True, recursive=True, keepext=False, regex=False)
    fileops.stage("*.txt", "asdf")
