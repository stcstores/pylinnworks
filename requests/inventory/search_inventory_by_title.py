from . get_inventory_items import GetInventoryItems
from . get_inventory_item_count import GetInventoryItemCount
from . inventory_view import InventoryView
from . get_inventory_views import GetInventoryViews
from . inventory_view_filter import InventoryViewFilter
from .. info . get_locations import GetLocations


class SearchInventoryByTitle(GetInventoryItems):

    def __init__(self, api, search_string, count=None, columns=None,
                 locations=None):
        if count is None:
            self.count = GetInventoryItemCount(api).item_count
        else:
            self.count = count
        self.view = InventoryView()
        if columns is None:
            self.view.columns = GetInventoryViews.standard_columns
        else:
            self.columns = columns
        self.view.filters = [InventoryViewFilter(
            field='Title', value=search_string, condition='contains'
        )]
        self.start = 0
        if locations is None:
            self.locations = [GetLocations.default]
        else:
            self.locations = locations
        super().__init__(api, start=0, count=self.count, view=self.view,
                         locations=self.locations)
