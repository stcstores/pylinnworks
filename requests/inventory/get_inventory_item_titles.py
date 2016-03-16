"""Requests channel titles for item """

from .. request import Request


class GetInventoryItemTitles(Request):
    url_extension = '/api/Inventory/GetInventoryItemTitles'

    def __init__(self, api, stock_id):
        self.stock_id = stock_id
        super().__init__(api)

    def get_data(self):
        data = {
            'inventoryItemId': self.stock_id
        }
        self.data = data
        return data
