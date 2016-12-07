#!/usr/bin/env python
import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "block_chain_bucks",
    version = "0.0.1",
    packages=["block_chain_bucks"],
    install_requires=["pycrypto"],
    long_description=read("README.md"),
)
