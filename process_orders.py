from pprint import pprint
import json
import requests

from linnworks_api import LinnworksAPI as LinnworksAPI
import lstools


def process_orders():
    api = LinnworksAPI(password='cosworth')

    while True:
        order_number = input('Order Number > ')
        guid = api.get_open_order_GUID_by_number(order_number)
        if guid == None:
            print('Error: GUID for ' + order_number + ' not found')
            continue
        api.process_order_by_GUID(guid)
        if api.get_open_order_GUID_by_number(order_number) is not None:
            print('Error: ' + order_number + ' may not be processed. GUID is ' + guid)
        else:
            print('OK')
        
