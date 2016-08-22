#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='pylinnworks',
    version='1.0',
    description='Wrapper for linnworks.net API',
    author='Luke Shiner',
    author_email='luke@lukeshiner.com',
    url='http://pylinnworks.lukeshiner.com',
    packages=find_packages(),
    install_requires=[
        'requests',
        'simplejson'],
    package_data={'': ['config.json']})
