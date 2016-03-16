"""Request count of inventory items. """

import json

from .. request import Request
from . get_inventory_views import GetInventoryViews
from .. info . get_locations import GetLocations
from . inventory_view import InventoryView


class GetInventoryItemCount(Request):
    url_extension = '/api/Inventory/GetInventoryItems'
    view = InventoryView()
    start = 0
    count = 1
    locations = []

    def __init__(self, api):
        self.locations = GetLocations(api).ids
        super().__init__(api)

    def process_response(self, response):
        self.item_count = response_dict['TotalItems']

    def get_data(self):
        data = {
            'view': self.view.to_json(),
            'startIndex': self.start,
            'itemsCount': self.count,
            'stockLocationIds': json.dumps(self.locations)
        }
        self.data = data
        return data
