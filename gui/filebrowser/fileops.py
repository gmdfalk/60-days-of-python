from datetime import datetime
import codecs
import dircache
import glob
import logging
import os
import re
import shutil
import sys
import time

import reporting


class Renamer(object):

    def __init__(self):
        self.recursive = False
