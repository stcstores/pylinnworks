"""Request inventory items.

Keyword arguments:
    start -- Index of first item to be returned. Default 0.
    count -- Number of items to be returned. Default 1.
    view: InventoryView ``JSON`` object to filter results. Default will
        return any item.
"""

import json

from pylinnworks.api_requests.request import Request


class GetInventoryItems(Request):
    url_server = 'https://eu3.linnworks.net'
    url_extension = '/api/Inventory/GetInventoryItems'

    def __init__(self, api_session, start=1, count=500, view=None,
                 locations=None):
        self.count = count
        self.start = start
        self.view = None
        self.locations = []
        self.view = view
        if locations is None:
            self.locations = locations
        else:
            self.locations = locations
        super().__init__(api_session)

    def get_data(self):
        data = {
            'view': self.view.to_json(),
            'startIndex': self.start,
            'itemsCount': self.count,
            'stockLocationIds': json.dumps(self.locations),
            'preloadChilds': json.dumps(False)
        }
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
