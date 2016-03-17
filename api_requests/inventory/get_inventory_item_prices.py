"""Requests channel prices for item """

from .. request import Request


class GetInventoryItemPrices(Request):
    url_extension = '/api/Inventory/GetInventoryItemPrices'

    def __init__(self, api_session, stock_id):
        self.stock_id = stock_id
        super().__init__(api_session)

    def get_data(self):
        data = {
            'inventoryItemId': self.stock_id
        }
        self.data = data
        return data
