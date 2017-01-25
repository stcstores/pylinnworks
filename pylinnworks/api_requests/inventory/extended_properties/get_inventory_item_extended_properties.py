"""Request extended properties for inventory item with stock ID stock_id """

from pylinnworks import PyLinnworks
from pylinnworks.api_requests.request import Request


class GetInventoryItemExtendedProperties(Request):
    url_extension = '/api/Inventory/GetInventoryItemExtendedProperties'

    def __init__(self, stock_id):
        self.stock_id = stock_id
        super().__init__(PyLinnworks)

    def get_data(self):
        data = {
            'inventoryItemId': self.stock_id
        }
        return data
