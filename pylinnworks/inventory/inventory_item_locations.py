"""Locations for inventory item."""

from pylinnworks import api_requests
from . inventory_item_location import InventoryItemLocation


class InventoryItemLocations:

    def __init__(self, stock_id):
        self.stock_id = stock_id
        data = api_requests.GetInventoryItemLocations(stock_id).response_dict
        print(data)
        self.locations = [InventoryItemLocation(
            stock_id, location_data) for location_data in data]

    def __repr__(self):
        return str(self.locations)

    def __iter__(self):
        for location in self.locations:
            yield location

    def __getitem__(self, index):
        return self.locations[index]

    def add_location(self, location):
        """Add inventory item to location."""
        api_requests.AddItemLocations(data=[(self.stock_id, location)])

    def get_location_by_ID(self, id_):
        for location in self.locations:
            if location.location_id == id_:
                return location
        raise IndexError('Item not in location with ID {}'.format(id_))

    def get_location_by_name(self, name):
        for location in self.locations:
            if location.location_name == name:
                return location
        raise IndexError('Item not in location with name {}'.format(name))
