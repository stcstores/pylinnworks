"""Request inventory items.

Keyword arguments:
    start -- Index of first item to be returned. Default 0.
    count -- Number of items to be returned. Default 1.
    view: InventoryView ``JSON`` object to filter results. Default will
        return any item.
"""

import json

from pylinnworks.api_requests.request import Request
from pylinnworks.functions import is_guid
from . get_inventory_views import GetInventoryViews
from . get_inventory_item_count import GetInventoryItemCount
from . inventory_view import InventoryView


class GetInventoryItems(Request):
    url_server = 'https://eu3.linnworks.net'
    url_extension = '/api/Inventory/GetInventoryItems'

    def __init__(self, api_session, start=1, count=100, view=None,
                 locations=None):
        self.count = count
        self.start = start
        self.view = None
        self.locations = []
        self.start = 0
        if view is None:
            self.view = GetInventoryViews(api_session)[0]
        else:
            self.view = view
        if locations is None:
            self.locations = api_session.locations.ids
        else:
            self.locations = locations
        super().__init__(api_session)

    def test_request(self):
        assert isinstance(self.view, InventoryView), \
            "View must be InventoryView."
        assert isinstance(self.start, int), \
            "Start must be of type int."
        assert isinstance(self.count, int), \
            "Count must be of type int."
        assert isinstance(self.locations, (list, set, tuple)), \
            "Locations must be dict or set."
        return super().test_request()

    def get_data(self):
        data = {
            'view': self.view.to_json(),
            'startIndex': self.start,
            'itemsCount': self.count,
            'stockLocationIds': json.dumps(self.locations),
            'preloadChilds': json.dumps(False)
        }
        return data

    def test_response(self, response):
        assert isinstance(response.json(), dict), \
            "Error message recieved: " + response.text
        return super().test_response(response)

    def process_response(self, response):
        self.result_count = len(self.response_dict['Items'])
        self.items_json = []
        self.item_titles = []
        self.skus = []
        self.guids = []
        for item in self.response_dict['Items']:
            self.items_json.append(item)
            self.item_titles.append(item['Title'])
            self.skus.append(item['SKU'])
            self.guids.append(item['Id'])
