# -*- coding: utf-8 -*-

# Learn more: https://github.com/msgill2017/strategy_backtester/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='strategy_back-tester',
    version='0.1.0',
    description='Manual option Strategy Back-tester',
    long_description=readme,
    author='Mandeep S Gill',
    author_email='msg8930@yahoo.com',
    url='https://mandeepsgill.netlify.app/',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

