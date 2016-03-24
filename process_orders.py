import os

from termcolor import colored, cprint
import colorama

from . linnworks_api_session import LinnworksAPISession


def process_orders(api_session):
    colorama.init()
    clear = "\n" * 100

    while True:
        order_number = input('Order Number > ')
        if order_number.lower() == 'c':
            os.system('cls')
            continue
        if order_number.lower() == 'exit':
            exit()
        guid = api_session.get_open_order_GUID_by_number(order_number)
        if guid is None:
            cprint('Error: GUID for ' + order_number + ' not found', 'red')
            continue
        order = api_session.get_open_order(guid)
        cprint(order.customer_name, 'yellow')
        if order.printed is not True:
            cprint('Order Not Printed!', 'red')
        if input('Process?') != '':
            cprint('Order Not Processed', 'red')
            continue
        api_session.process_order_by_GUID(guid)
        if api_session.get_open_order_GUID_by_number(order_number) is not None:
            cprint(
                'Error: ' + order_number + ' may not be processed.', 'red')
        else:
            cprint(order_number + ' Processed', 'green')
