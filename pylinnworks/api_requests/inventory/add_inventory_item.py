"""Requests creation of new inventory item. """

import json

from pylinnworks.api_requests.request import Request


class AddInventoryItem(Request):
    url_extension = '/api/Inventory/AddInventoryItem'

    def __init__(
            self, api_session, stock_id=None, sku=None, title='', barcode=''):
        if stock_id is None:
            raise TypeError('stock_id must by type str')
        self.stock_id = str(stock_id)
        if sku is None:
            raise TypeError('sku must be type str')
        self.sku = str(sku)
        self.title = str(title)
        self.barcode = str(barcode)
        super().__init__(api_session)

    def get_data(self):
        inventory_item = {
            'StockItemId': str(self.stock_id),
            'ItemNumber': str(self.sku),
            'ItemTitle': str(self.title),
            'BarcodeNumber': str(self.barcode),
        }
        data = {'inventoryItem': json.dumps(inventory_item)}
        return data
