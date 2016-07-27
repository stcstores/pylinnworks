#!/usr/bin/env python

from distutils.core import setup

setup(
    name='pylinnworks',
    version='1.0',
    description='Wrapper for linnworks.net API',
    author='Luke Shiner',
    author_email='luke@lukeshiner.com',
    url='http://pylinnworks.lukeshiner.com',
    packages=[
        'pylinnworks',
        'pylinnworks.api_requests',
        'pylinnworks.api_requests.import_export',
        'pylinnworks.api_requests.inventory',
        'pylinnworks.api_requests.inventory.extended_properties',
        'pylinnworks.api_requests.inventory.images',
        'pylinnworks.api_requests.inventory.update_inventory',
        'pylinnworks.api_requests.orders',
        'pylinnworks.api_requests.processed_orders',
        'pylinnworks.api_requests.settings',
        'pylinnworks.inventory',
        'pylinnworks.orders',
        'pylinnworks.settings'],
    package_data={'': ['config.json']})
