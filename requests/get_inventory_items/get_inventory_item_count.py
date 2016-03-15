"""Request count of inventory items. """

import json

from . get_inventory_items import GetInventoryItems
from . get_inventory_views import GetInventoryViews
from .. info . get_locations import GetLocations
from . inventory_view import InventoryView


class GetInventoryItemCount(GetInventoryItems):
    view = InventoryView()
    start = 0
    count = 1
    locations = []

    def __init__(self, api):
        super(GetInventoryItems, self).__init__(api)
        self.locations = GetLocations(api).ids

    def process_response(self, response):
        self.item_count = response.json()['TotalItems']
