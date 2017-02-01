from pylinnworks import Settings
from pylinnworks import api_requests


class InventoryItemLocation:

    def __init__(self, stock_id, data):
        self.stock_id = stock_id
        self.location = Settings.get_location_by_ID(data['StockLocationId'])
        self.bin_rack = data['BinRack']

    def __repr__(self):
        return '{} location: {}'.format(self.location.name, self.bin_rack)

    @property
    def location_name(self):
        return self.location.name

    @property
    def location_id(self):
        return self.location.guid

    def save(self):
        api_requests.UpdateItemLocations(
            [(self.stock_id, self.bin_rack, self.location)])
