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


def get_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    config = json.load(open(config_path, 'r'))
    try:
        config = json.load(open(config_path, 'r'))
    except:
        return None
    return config


def get_api_session():
    config = get_config()
    if config is not None:
        return LinnworksAPISession(
            application_id=config['application_id'],
            application_secret=config['application_secret'],
            server=config['server'],
            application_token=config['application_token'])


class PyLinnworks:
    api_session = get_api_session()

    def __init__(
            self, application_id=None, application_secret=None,
            application_token=None, server=None):
        self.api_session = LinnworksAPISession(
            application_id=application_id,
            application_secret=application_secret, server=server,
            application_token=application_token)

    @classmethod
    def Settings(self):
        return Settings(PyLinnworks.api_session)

    @classmethod
    def Manifests(self):
        return Manifests(PyLinnworks.api_session)

    @classmethod
    def Linking(self):
        return Linking(PyLinnworks.api_session)

    @classmethod
    def ProcessedOrders(self):
        return ProcessedOrders(PyLinnworks.api_session)
