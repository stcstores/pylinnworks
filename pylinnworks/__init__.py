"""This module contains provides classes for making requests to
api.linnworks.net
"""

from . import settings
from . import orders
from . import inventory
from . shipping import *
from . functions import *
from . linnworks_api_session import LinnworksAPISession
from . exceptions import *
from . processed_orders import ProcessedOrders


def get_api_session():
    return LinnworksAPISession()
