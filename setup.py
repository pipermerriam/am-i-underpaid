#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pip.download import PipSession
from pip.req import parse_requirements
import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import disparity
version = disparity.__version__

session = PipSession()

requirements = [
    str(req.req) for req in parse_requirements('requirements.txt', session=session)
]

setup(
    name='Am I Underpaid',
    version=version,
    author='',
    author_email='pipermerriam@gmail.com',
    url='https://github.com/pipermerriam/am-i-underpaid',
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    license="MIT",
    scripts=['disparity/manage.py'],
)