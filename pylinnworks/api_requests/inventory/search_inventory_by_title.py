from . get_inventory_items import GetInventoryItems
from . get_inventory_item_count import GetInventoryItemCount
from . inventory_view import InventoryView
from . get_inventory_views import GetInventoryViews
from . inventory_view_filter import InventoryViewFilter


class SearchInventoryByTitle(GetInventoryItems):

    def __init__(self, api_session, search_string, count=None, columns=None,
                 locations=None):
        if count is None:
            self.count = GetInventoryItemCount(api_session).item_count
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
            self.locations = [self.api_session.locations['Default'].guid]
        else:
            self.locations = locations
        super().__init__(
            api_session, start=0, count=self.count, view=self.view,
            locations=self.locations)
