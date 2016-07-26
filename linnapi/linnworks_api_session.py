#!/usr/bin/env python3

"""This module contains the main ``LinnworksAPI`` class, the wrapper class for
the linnworks.net API.
"""

import os
import requests
import json
import uuid
import re
from pprint import pprint

from linnapi.settings import Categories
from linnapi.settings import PackageGroups
from linnapi.settings import ShippingMethods
from linnapi.settings import Locations
from linnapi.settings import PostageServices
from linnapi.settings import Channels
from linnapi.exceptions import *


class LinnworksAPISession:
    """Main wrapper class for linnworks.net API. Allows authentication with
    API and provides methods for many common API requests.
    """

    def __init__(self, *kwargs):
        """
        Create session with linnworks.net API
        """
        self.session = requests.Session()
        self.config_path = os.path.join(
            os.path.dirname(__file__), 'config.json')
        self.load_config()
        if self.application_token == '':
            self.set_application_token()
        self.token = self.get_token()
        self.get_settings()

    def set_application_token(self):
        print('Application Token Required')
        try:
            app = GetApplicationTokenApp()
            app.root.mainloop()
            token = app.token
        except:
            token = input('Application Token: ')
        self.application_token = token
        self.update_config_file(
            token, self.server, self.application_id, self.application_secret)

    def get_config(self):
        config = json.load(open(self.config_path, 'r'))
        return config

    def load_config(self):
        self.config = self.get_config()
        self.server = self.config['server']
        self.application_id = self.config['application_id']
        self.application_secret = self.config['application_secret']
        self.application_token = self.config['application_token']

    def update_config(self):
        self.update_config_file(
            self.server, self.application_id, self.application_secret,
            self.application_token)

    def update_config_file(
            self, application_token, server, application_id,
            application_secret):
        config = {
            'server': server,
            'application_id': application_id,
            'application_secret': application_secret,
            'application_token': application_token}
        json.dump(
            config, open(self.config_path, 'w'), indent=4, sort_keys=True)

    def get_token(self):
        url = 'https://api.linnworks.net//api/Auth/AuthorizeByApplication'
        data = {
            'applicationId': self.application_id,
            'applicationSecret': self.application_secret,
            'token': self.application_token}
        try:
            request = self.session.post(url, data=data)
        except:
            raise
        request.raise_for_status()
        try:
            token = request.json()['Token']
        except:
            raise InvalidResponse(request)
        return token

    def test_login(self):
        url = self.server + '/api/Stock/SKUExists'
        data = {'SKU': 'None'}
        params = {'token': self.token}
        try:
            response = self.make_request(url, data=data, params=params)
        except:
            raise
        if response.text in ('true', 'false'):
            return True
        return False

    def make_request(self, url, data=None, params=None, files=None):
        """Request resource URL

        Arguments:
            url -- URL of resource to be requested.

        Keyword arguments:
            data --  dict containing POST request variables. (Default None)
            params --  dict containing GET request variables. (Default None)

        Returns:
            ``requests.Request`` object.
        """
        request = self.session.post(
            url, data=data, params=params, files=files)
        return request

    def request(self, url, data=None, params={}, files=None):
        """Add authentication variables and make API request.

        Arguments:
            url -- URL to request.

        Keyword Arguments:
            data -- ``dict`` of GET variables (Default None)

        Returns:
            ``requests.Request`` object.
        """
        params['token'] = self.token
        request = self.make_request(url, data=data, params=params, files=files)
        return request

    def get_settings(self):
        self.categories = Categories(self)
        self.package_groups = PackageGroups(self)
        self.shipping_methods = ShippingMethods(self)
        self.locations = Locations(self)
        self.postage_services = PostageServices(self)
        self.channels = Channels(self)


class GetApplicationTokenApp:
    def __init__(self):
        import tkinter
        self.root = tkinter.Tk()
        self.token_var = tkinter.StringVar()
        self.input_label = tkinter.Label(
            self.root, text='Application Token: ')
        self.entry = tkinter.Entry(self.root, textvariable=self.token_var)
        self.button = tkinter.Button(
            self.root, text='Confirm', command=self.set_token)
        self.input_label.grid(row=0, column=0)
        self.entry.grid(row=0, column=1)
        self.button.grid(row=0, column=2)

    def set_token(self):
        self.token = self.token_var.get()
        self.root.destroy()
