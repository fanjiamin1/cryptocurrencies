#!/usr/bin/env python
import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pychat",
    version = "0.0.1",
    packages=["pychat"],
    long_description=read("README.md"),
)
