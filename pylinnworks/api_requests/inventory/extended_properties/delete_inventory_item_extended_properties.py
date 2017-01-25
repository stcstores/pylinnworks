import json

from pylinnworks import PyLinnworks
from pylinnworks.api_requests.request import Request


class DeleteInventoryItemExtendedProperties(Request):

    url_extension = '/api/Inventory/DeleteInventoryItemExtendedProperties'

    def __init__(self, stock_id=None, property_ids=[]):
        self.stock_id = stock_id
        self.property_ids = property_ids
        super().__init__(PyLinnworks)

    def get_data(self):
        data = {
            'inventoryItemId': self.stock_id,
            'inventoryItemExtendedPropertyIds': json.dumps(self.property_ids)}
        self.data = data
        return self.data
