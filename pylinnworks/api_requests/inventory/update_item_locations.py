"""Update bin/rack for inventory item in location."""

from uuid import uuid4
import json

from pylinnworks.api_requests.request import Request
from pylinnworks import PyLinnworks


class UpdateItemLocations(Request):

    url_extension = '/api/Inventory/UpdateItemLocations'

    def __init__(self, data):
        self.updates = []
        for update in data:
            self.add_update(update)
        super().__init__(PyLinnworks)

    @staticmethod
    def make_update_object(
            location_id, location_name, bin_rack, stock_id, id_=None,
            is_changed=True):
        if id_ is None:
            id_ = str(uuid4())
        return {
            'StockLocationId': location_id,
            'LocationName': location_name,
            'BinRack': bin_rack,
            'StockItemId': stock_id,
            'id': id_,
            'IsChanged': is_changed
        }

    def add_update(self, update):
        stock_id, bin_rack, location = update
        self.updates.append(self.make_update_object(
            location.guid, location.name, bin_rack, stock_id))

    def get_data(self):
        data = {'itemLocations': json.dumps(self.updates)}
        return data
