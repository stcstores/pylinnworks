import os

from termcolor import colored, cprint
import colorama

from . linnworks_api import LinnworksAPI as LinnworksAPI


def process_orders():
    colorama.init()
    api = LinnworksAPI(username='stcstores@yahoo.com', password='cosworth')
    clear = "\n" * 100

    while True:
        order_number = input('Order Number > ')
        if order_number.lower() == 'c':
            os.system('cls')
            continue
        if order_number.lower() == 'exit':
            exit()
        guid = api.get_open_order_GUID_by_number(order_number)
        if guid is None:
            cprint('Error: GUID for ' + order_number + ' not found', 'red')
            continue
        if not api.order_is_printed(guid):
            cprint('Order Not Printed!', 'red')
            response = input('process? y / n >').lower()
            if response not in ('y', 'yes'):
                continue
        api.process_order_by_GUID(guid)
        if api.get_open_order_GUID_by_number(order_number) is not None:
            cprint('Error: ' + order_number + ' may not be processed. GUID is ' + guid, 'red')
        else:
            cprint('OK', 'green')
