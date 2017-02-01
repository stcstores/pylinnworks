"""Get location an bin/rack information for inventory item."""

from pylinnworks.api_requests.request import Request
from pylinnworks import PyLinnworks


class GetInventoryItemLocations(Request):

    url_extension = '/api/Inventory/GetInventoryItemLocations'

    def __init__(self, stock_id):
        self.stock_id = stock_id
        super().__init__(PyLinnworks)

    def get_data(self):
        return {'inventoryItemId': self.stock_id}
