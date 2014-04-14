#!/usr/bin/env python2

import os


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()


_name = "demibot"
_license = "MIT"


setup(
    name=_name,
    description="A modular IRC bot",
    long_description=read("README.md"),
    version="0.2",
    license=_license,
    url="https://github.com/mikar/%s" % _name,
    author="Max Demian",
    author_email="mikar@gmx.de",
    packages=[_name, _name + "/modules"],
    package_data={_name + "/modules": ["*.txt"]},
    install_package_data=True,
    entry_points={
                  "console_scripts": [
                      "{0} = {0}.main:main".format(_name),
                  ],
              }
)
