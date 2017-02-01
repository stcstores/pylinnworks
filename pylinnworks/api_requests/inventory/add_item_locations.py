"""Add inventory location to inventory item."""

from uuid import uuid4
import json

from pylinnworks.api_requests.request import Request
from pylinnworks import PyLinnworks


class AddItemLocations(Request):

    url_extension = '/api/Inventory/AddItemLocations'

    def __init__(self, data):
        """Adds stock locations to inventory items.

        Args:
            data (list): List of tuples where each tuple contains the stock
                ID (GUID) of the inventory item and the Location object
                containing the location to be added - (stock_id, location).
        """
        self.item_locations = []
        for item_location in data:
            stock_id, location = item_location
            self.add_item_locations(stock_id, location)
        super().__init__(PyLinnworks)

    @staticmethod
    def make_item_location(
            cls, stock_id, location_id, location_name, is_added, id_):
        return {
            'StockItemId': stock_id,
            'StockLocationId': location_id,
            'LocationName': location_name,
            'isAdded': is_added,
            'id': id_
        }

    def get_data(self):
        data = {'itemLocations': json.dumps(self.item_locations)}
        return data

    def add_item_locations(self, stock_id, location):
        item_location = self.make_item_location(
            stock_id, location.guid, location.name, True, str(uuid4()))
        self.item_locations.append(item_location)
