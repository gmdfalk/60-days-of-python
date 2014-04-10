#!/usr/bin/env python2

import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()

setup(
    name = "demibot",
    description = "a multi-purpose IRC bot",
    long_description = read("README.md"),
    keywords = "irc bot",
    version = "0.1",
    license = "MIT",
    url = "https://github.com/mikar/demibot",
    author = "Max Demian",
    author_email = "mikar@gmx.de",
    #~ install_requires = ['nose'],
    packages = ["demibot", "demibot/modules"],
    entry_points = {
                  'console_scripts': [
                      'demibot = demibot.main:main',                  
                  ],              
              }
)
