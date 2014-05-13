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
import sys

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

    def stage(self, expression, path=None):
        if path is None:
            path = os.getcwd()

        targets = self.get_targets(path)
        print targets
        matches = self.match_targets(targets, expression)
        print matches

    def get_targets(self, path):
        "Creates a list of files and/or directories to work with."
        targets = []
        for root, dirs, files in os.walk(path):
            root += "/"
            if self.dirsonly:
                target = [(root, d) for d in dirs]
            elif self.filesonly:
                target = []
                for f in files:
                    fname, ext = os.path.splitext(f)
                    target.append((root, fname, ext))
            else:
                target = [(root, d) for d in dirs]
                for f in files:
                    fname, ext = os.path.splitext(f)
                    target.append((root, fname, ext))

            if self.hidden:
                targets.extend(target)
            else:
                targets.extend(i for i in target if not i[2].startswith("."))

            # Exit before the second loop for non-recursive searches.
            if not self.recursive:
                break

        return targets

    def match_targets(self, targets, expression):
        "Finds regex/glob matches in the list of targets."
        matches = []
        for i in targets:
            pass
        # [i for i, j in zip(a, b) if i != j]
        return matches

    def commit(self):
        pass

    def rollback(self):
        pass


if __name__ == "__main__":
    log = reporting.create_logger()
    reporting.configure_logger(log)
    fileops = FileOps(hidden=True, recursive=False)
    fileops.stage("asdf")
