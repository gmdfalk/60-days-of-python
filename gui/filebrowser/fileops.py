# from datetime import datetime
# import codecs
# import dircache
# import shutil
# import time
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
                 noclobber=False, count=None, regex=False, quiet=False):
        self.recursive = recursive
        self.hidden = hidden
        self.dirsonly = dirsonly
        self.filesonly = False if dirsonly else filesonly
        self.simulate = simulate
        self.interactive = interactive
        self.prompt = prompt
        self.noclobber = noclobber
        self.count = count
        self.regex = regex
        self.log = logging.getLogger()

    def stage(self, expression, path=None):
        if path is None:
            path = os.getcwd()

        targets = self.get_targets(path)
        print targets

    def get_targets(self, path):
        targets = []
        for root, dirs, files in os.walk(path):
            root += "/"
            if self.dirsonly:
                target = [root + d for d in dirs]
            elif self.filesonly:
                target = [root + f for f in files]
            else:
                target = [root + d for d in dirs] + [root + f for f in files]

            if self.hidden:
                targets.extend(target)
            else:
                targets.extend(i for i in target if not i.startswith("."))

            if not self.recursive:
                break

        return targets

    def get_targetlist(self, expression):
        path = None
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        glob.glob(os.path.join(path, "*"))

    def commit(self):
        pass

    def rollback(self):
        pass


if __name__ == "__main__":
    log = reporting.create_logger()
    reporting.configure_logger(log)
    fileops = FileOps(filesonly=True, hidden=True, recursive=True)
    fileops.stage("asdf")
