"""This module contains provides classes for making requests to
api.linnworks.net
"""
import os
import json
import requests

from . linnworks_api_session import LinnworksAPISession
from . settings import Settings
from . shipping import Manifests
from . processed_orders import ProcessedOrders
from . linking import Linking
from . import exceptions
from . import settings  # DEPRICATED
from . import orders  # DEPRICATED
from . import inventory  # DEPRICATED
from . shipping import *  # DEPRICATED
from . functions import *  # DEPRICATED


config_path = os.path.join(os.path.dirname(__file__), 'config.json')


class PyLinnworks:
    config = {
        'application_id': None,
        'application_secret': None,
        'application_token': None,
        'server': None}
    session = requests.Session()
    try:
        config.update(json.loads(config_path))
    except:
        pass

    @classmethod
    def connect(
            cls, config_file=None, config_path=None, application_id=None,
            application_secret=None, application_token=None, server=None,
            token=None):
        if config_file is not None:
            cls.load_config(config_file)
        if config_path is not None:
            cls.load_config_from_file(config_path)
        if application_id is not None:
            cls.application_id = application_id
        if application_secret is not None:
            cls.application_secret = application_secret
        if application_token is not None:
            cls.application_token = application_token
        if server is not None:
            cls.server = server
        cls.token = cls.get_token()

    @classmethod
    def load_config(cls, config):
        cls.application_id = config['application_id']
        cls.application_secret = config['application_secret']
        cls.application_token = config['application_token']
        cls.server = config['server']

    @classmethod
    def load_config_from_file(cls, config_path):
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        cls.load_config(config)

    @property
    def application_id(cls):
        return cls.config['appilcation_id']

    @application_id.setter
    def application_id(cls, application_id):
        cls.config['application_id'] = application_id

    @property
    def application_secret(cls):
        return cls.config['appilcation_secret']

    @application_secret.setter
    def application_secret(cls, application_secret):
        cls.config['application_secret'] = application_secret

    @property
    def application_token(cls):
        return cls.config['application_token']

    @application_token.setter
    def application_token(cls, application_token):
        cls.config['application_token'] = application_token

    @property
    def server(cls):
        return cls.config['server']

    @server.setter
    def server(cls, server):
        cls.config['server'] = server

    @property
    def token(cls):
        return cls.api_session.token

    @token.setter
    def token(cls, token):
        cls.api_session.token = token

    @classmethod
    def get_token(cls):
        cls.api_session.token = cls.api_session.get_token()

    @classmethod
    def Settings(cls):
        return Settings(cls)

    @classmethod
    def Manifests(cls):
        return Manifests(cls)

    @classmethod
    def Linking(cls):
        return Linking(cls)

    @classmethod
    def ProcessedOrders(cls):
        return ProcessedOrders(cls)

    @classmethod
    def get_token(cls):
        url = ''.join([cls.server, '/api/Auth/AuthorizeByApplication'])
        data = {
            'applicationId': cls.application_id,
            'applicationSecret': cls.application_secret,
            'token': cls.application_token}
        request = cls.session.post(url, data=data)
        request.raise_for_status()
        try:
            token = request.json()['Token']
        except:
            raise InvalidResponse(request)
        return token

    @classmethod
    def test_login(cls):
        url = cls.server + '/api/Stock/SKUExists'
        data = {'SKU': 'None'}
        params = {'token': cls.token}
        try:
            response = cls.make_request(url, data=data, params=params)
        except:
            raise
        if response.text in ('true', 'false'):
            return True
        return False

    @classmethod
    def make_request(cls, url, data=None, params=None, files=None):
        """Request resource URL

        Arguments:
            url -- URL of resource to be requested.

        Keyword arguments:
            data --  dict containing POST request variables. (Default None)
            params --  dict containing GET request variables. (Default None)

        Returns:
            ``requests.Request`` object.
        """
        request = cls.session.post(
            url, data=data, params=params, files=files)
        return request

    @classmethod
    def request(cls, url, data=None, params={}, files=None):
        """Add authentication variables and make API request.

        Arguments:
            url -- URL to request.

        Keyword Arguments:
            data -- ``dict`` of GET variables (Default None)

        Returns:
            ``requests.Request`` object.
        """
        params['token'] = cls.token
        request = cls.make_request(url, data=data, params=params, files=files)
        return request
