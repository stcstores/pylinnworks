import os
import json
import statistics

from termcolor import colored, cprint
import colorama

from lstools import DatabaseTable

import linnapi


class WeightsDatabase(DatabaseTable):
    def __init__(self):
        self.stock_id_field = 'stock_id'
        self.weights_field = 'weights_string'
        super().__init__(database='linnworks', table='weights')

    def add_weight(self, stock_id, weight):
        if self.stock_id_exists(stock_id):
            weight_list = self.get_weight_list(stock_id)
        else:
            weight_list = []
        weight_list.append(weight)
        weight_string = json.dumps(weight_list)
        query = "INSERT INTO {} ({}, {}) VALUES ".format(
            self.table, self.stock_id_field, self.weights_field)
        query += "('{}', '{}') ON DUPLICATE KEY UPDATE {}=VALUES({})".format(
            stock_id, weight_string, self.weights_field, self.weights_field)
        self.query(query)
        assert(weight_list == self.get_weight_list(stock_id))

    def get_weight_list(self, stock_id):
        query = "SELECT {} FROM {} WHERE {}='{}'".format(
            self.weights_field, self.table, self.stock_id_field, stock_id)
        result = self.query(query)
        return json.loads(result[0][0])

    def get_stock_ids(self):
        query = "SELECT {} FROM {}".format(self.stock_id_field, self.table)
        result = self.query(query)
        stock_ids = [record[0] for record in result]
        return stock_ids

    def stock_id_exists(self, stock_id):
        stock_ids = self.get_stock_ids()
        if stock_id in stock_ids:
            return True
        return False

    def get_weight(stock_id):
        weight_list = self.get_weight_list(stock_id)
        return statistics.mean(weight_list)


def process_orders(api_session, weights=False):
    colorama.init()
    if weights is True:
        weight_database = WeightsDatabase()

    while True:
        order_number = input('Order Number > ')
        if order_number.lower() == 'c':
            os.system('cls')
            continue
        if order_number.lower() == 'exit':
            return 0
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
            if weights is True:
                process_weight(weight_database, order)


def process_weight(weight_database, order):
    if len(order.items) == 1 and order.items[0].quantity == 1:
        item = order.items[0]
        item_weight = input('Weight: ')
        if item_weight.isdigit():
            item_weight = int(item_weight)
            if item_weight > 0 and item_weight < 9999:
                weight_database.add_weight(
                    item.stock_id, item_weight)
                cprint('Added {}g to weights for {}'.format(
                    item_weight, item.title), 'green')
