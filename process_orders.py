import os

from termcolor import colored, cprint
import colorama

import linnapi


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
        guid_request = linnapi.api_requests.GetOpenOrderIDByOrderOrReferenceID(
            api_session, order_number)
        guid = guid_request.response_dict
        if guid is None:
            cprint('Error: GUID for ' + order_number + ' not found', 'red')
            continue
        order = linnapi.orders.OpenOrder(api_session, load_order_id=guid)
        cprint(order.customer_name, 'yellow')
        if order.invoice_printed is not True:
            cprint('Order Not Printed!', 'red')
        if input('Process?') != '':
            cprint('Order Not Processed', 'red')
            continue
        process_success = order.process()
        if process_success is False:
            cprint(
                'Error: ' + order_number + ' may not be processed.', 'red')
        else:
            cprint(order_number + ' Processed', 'green')
