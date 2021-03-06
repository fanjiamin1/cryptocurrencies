#!/usr/bin/env python
import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "big_brother_bucks",
    version = "0.0.1",
    packages=["big_brother_bucks"],
    install_requires=["pycrypto mysqlclient"],
    long_description=read("README.md"),
)
