# from datetime import datetime
# import codecs
# import dircache
# import shutil
# import time
# TODO: Exclude option
import fnmatch
import glob
import logging
import os
import re

import reporting


class FileOps(object):

    def __init__(self, dirsonly=False, filesonly=False, recursive=False,
                 hidden=False, simulate=False, interactive=False, prompt=False,
                 noclobber=False, keepext=True, count=None, regex=False,
                 quiet=False, exclude=None):
        self.dirsonly = dirsonly
        self.filesonly = False if dirsonly else filesonly
        self.recursive = recursive  # Look for files recursively
        self.hidden = hidden  # Look at hidden files and directories, too.
        self.simulate = simulate  # Simulate renaming and dump result to stdout.
        self.interactive = interactive  # Confirm before overwriting.
        self.prompt = prompt  # Confirm all rename actions.
        self.noclobber = noclobber  # Don't overwrite anything.
        self.keepext = keepext  # Don't modify extensions.
        self.count = count  # Adds numerical index at position count in target.
        self.regex = regex  # Use regular expressions instead of glob/fnmatch.
        self.quiet = quiet  # No logging.
        self.exclude = exclude  # List of strings to exclude from targets.

    def stage(self, srcpat, destpat, path=None):
        if path is None:
            path = os.getcwd()

        targets = self.find_targets(srcpat, path)
        print targets
        modtargets = self.modify_targets(targets, srcpat, destpat)
#         matches = self.match_targets(targets, expression)
#         print matches
        # [i for i, j in zip(a, b) if i != j]

    def split_files(self, files, root, srcpat):
        target = []
        for f in files:
            fname, ext = os.path.splitext(f)
            if self.match(srcpat, fname, ext):
                target.append((root, fname, ext))
        return target

    def joinext(self, target):
        if len(target) > 2:
            target = (target[1], target[2])
        name = target[0]
        if not self.keepext:
            try:
                name += target[1]
            except IndexError:
                pass
        return name

    def match(self, srcpat, *target):
        "Searches target for pattern and returns True/False respectively."
        name = self.joinext(target)
        if self.regex:
            if re.search(srcpat, name):
                return True
        else:
            if fnmatch.fnmatch(name, srcpat):
                return True

        return False

    def find_targets(self, srcpat, path):
        "Creates a list of files and/or directories to work with."
        targets = []
        for root, dirs, files in os.walk(path):
            root += "/"
            if self.dirsonly:
                target = [(root, d) for d in dirs if self.match(srcpat, d)]
            elif self.filesonly:
                self.split_files(files, root, srcpat)
            else:
                target = [(root, d) for d in dirs if self.match(srcpat, d)]
                target += self.split_files(files, root, srcpat)

            if self.hidden:
                targets.extend(target)
            else:
                targets.extend(i for i in target if not i[1].startswith("."))

            # Exit before the second loop for non-recursive searches.
            if not self.recursive:
                break

        return targets

    def modify_targets(self, targets, srcpat, destpat):
        if not self.regex:
            srcpat = fnmatch.translate(srcpat)
            destpat = fnmatch.translate(destpat)
        print srcpat, destpat
        srcrx = re.compile(srcpat)
        destrx = re.compile(destpat)
        for target in targets:
            name = self.joinext(target)
            match = srcrx.search(name)

    def commit(self):
        pass

    def rollback(self):
        pass


if __name__ == "__main__":
    log = reporting.create_logger()
    reporting.configure_logger(log)
    fileops = FileOps(hidden=True, recursive=False, keepext=False, regex=False)
    fileops.stage("demi*", "*")
