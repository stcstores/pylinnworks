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

    def __init__(self, api_session):
        self.locations = GetLocations(api_session).ids
        super().__init__(api_session)

    def process_response(self, response):
        self.item_count = self.response_dict['TotalItems']

    def get_data(self):
        data = {
            'view': self.view.to_json(),
            'startIndex': self.start,
            'itemsCount': self.count,
            'stockLocationIds': json.dumps(self.locations)
        }
        self.data = data
        return data
