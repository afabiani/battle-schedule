#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from distutils.core import setup

from setuptools import find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name="battle_schedule",
    version="1.0",
    author="afabiani",
    author_email="alessio.fabiani@gmail.com",
    description="battle_schedule",
    # long_description=(read('README.md')),
    # Full list of classifiers can be found at:
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
    license="GPL",
    keywords="battle_schedule django",
    url='https://github.com/afabiani/battle-schedule',
    packages=find_packages(),
    dependency_links=[],
    include_package_data=True,
)
