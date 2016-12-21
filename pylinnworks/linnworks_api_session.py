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

from pylinnworks.settings import Categories
from pylinnworks.settings import PackageGroups
from pylinnworks.settings import ShippingMethods
from pylinnworks.settings import Locations
from pylinnworks.settings import PostageServices
from pylinnworks.settings import Channels
from pylinnworks.exceptions import *


class LinnworksAPISession:
    """Main wrapper class for linnworks.net API. Allows authentication with
    API and provides methods for many common API requests.
    """

    config_path = os.path.join(os.path.dirname(__file__), 'config.json')

    def __init__(
            self, application_id=None, application_secret=None, server=None,
            application_token=None, token=None):
        """
        Create session with linnworks.net API
        """
        self.session = requests.Session()
        self.application_id = application_id
        self.application_secret = application_secret
        self.server = server
        self.application_token = application_token
        if token is None:
            self.token = self.get_token()
        else:
            self.token = token

    def get_token(self):
        url = ''.join([self.server, '/api/Auth/AuthorizeByApplication'])
        data = {
            'applicationId': self.application_id,
            'applicationSecret': self.application_secret,
            'token': self.application_token}
        request = self.session.post(url, data=data)
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
