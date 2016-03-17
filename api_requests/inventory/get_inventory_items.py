"""Request inventory items.

Keyword arguments:
    start -- Index of first item to be returned. Default 0.
    count -- Number of items to be returned. Default 1.
    view: InventoryView ``JSON`` object to filter results. Default will
        return any item.
"""

import json

from .. request import Request
from . get_inventory_views import GetInventoryViews
from .. info . get_locations import GetLocations
from . get_inventory_item_count import GetInventoryItemCount


class GetInventoryItems(Request):
    url_extension = '/api/Inventory/GetInventoryItems'
    start = 0
    count = 0
    view = None
    locations = []

    def __init__(self, api_session, start=0, count=0, view=None,
                 locations=None):
        self.start = 0
        if count == 0:
            self.count = GetInventoryItemCount(api_session).item_count
        else:
            self.count = count
        if view is None:
            self.view = GetInventoryViews(api_session)[0]
        else:
            self.view = view
        if locations is None:
            self.locations = GetLocations(api_session).ids
        else:
            self.location = locations
        super().__init__(api_session)

    def get_data(self):
        data = {
            'view': self.view.to_json(),
            'startIndex': self.start,
            'itemsCount': self.count,
            'stockLocationIds': json.dumps(self.locations)
        }
        self.data = data
        return data

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
