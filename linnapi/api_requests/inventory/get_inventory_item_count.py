"""Request count of inventory items. """

import json

from linnapi.api_requests.request import Request
from . get_inventory_views import GetInventoryViews
from . inventory_view import InventoryView


class GetInventoryItemCount(Request):
    url_extension = '/api/Inventory/GetInventoryItems'
    view = InventoryView()
    start = 0
    count = 1
    locations = []

    def __init__(self, api_session):
        self.locations = api_session.locations.ids
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
        return data

    def test_response(self, response):
        assert isinstance(response.json(), dict), \
            "Error message recieved: " + response.text
        return super().test_response(response)
