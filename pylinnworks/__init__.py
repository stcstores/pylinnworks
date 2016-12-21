"""This module contains provides classes for making requests to
api.linnworks.net
"""
import os
import json

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
    api_session = None
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
        cls.api_session = LinnworksAPISession(
            application_id=cls.application_id,
            application_secret=cls.application_secret,
            application_token=cls.application_token,
            server=cls.server, token=token)

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
        return Settings(cls.api_session)

    @classmethod
    def Manifests(cls):
        return Manifests(cls.api_session)

    @classmethod
    def Linking(cls):
        return Linking(cls.api_session)

    @classmethod
    def ProcessedOrders(cls):
        return ProcessedOrders(cls.api_session)


def load_config_from_file():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    try:
        config = json.load(open(config_path, 'r'))
    except:
        return None
    PyLinnworks.config.update(config)
