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

from . inventory_item import InventoryItem as InventoryItem
from . basic_item import BasicItem as BasicItem
from . open_order import OpenOrder as OpenOrder
from . inventory import Inventory as Inventory


class LinnworksAPI:
    """Main wrapper class for linnworks.net API. Allows authentication with
    API and provides methods for many common API requests.
    """

    def __init__(self, username=None, password=None):
        """Authenticate user and set ``self.token`` and ``self.server``
        variables. If password argument is None request password form user as
        ``input()``.

        Keyword Arguments:
            username -- Linnworks username (Default None)
            password -- Linnworks password (Default None)
        """
        self.session = requests.Session()
        if username is None:
            self.username = input('Linnworks Username: ')
        else:
            self.username = username
        if password is None:
            self.password = input('Linnworks Password: ')
        else:
            self.password = password
        self.get_token()

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
        response = self.session.post(
            url, data=data, params=params, files=files)
        return response

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
        return self.make_request(url, data=data, params=params, files=files)

    def get_token(self):
        """Make authentication requests and set ``self.token`` and
        ``self.server`` accordingly.
        """
        login_url = 'https://api.linnworks.net//api/Auth/Multilogin'
        auth_url = 'https://api.linnworks.net//api/Auth/Authorize'
        login_data = {'userName': self.username, 'password': self.password}
        multilogin = self.make_request(login_url, login_data).json()
        self.user_id = multilogin[0]['Id']
        auth_data = login_data
        auth_data['userId'] = self.user_id
        authorize = self.make_request(auth_url, auth_data).json()
        self.token = authorize['Token']
        self.server = authorize['Server']
