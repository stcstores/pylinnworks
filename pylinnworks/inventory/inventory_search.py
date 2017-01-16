from pylinnworks.api_requests import GetInventoryItemCount
from .. settings import Settings
from . inventory_view import InventoryView
from . inventory_view_filter import InventoryViewFilter
from . inventory_view_column import ALL_COLUMNS
from pylinnworks.api_requests import GetInventoryItems
from . inventory_list import InventoryList


class InventorySearch:

    def __init__(self, api_session, filters=[], locations=None, columns=None):
        self.api_session = api_session
        self.view = InventoryView()
        if columns is None:
            self.columns = ALL_COLUMNS
        else:
            self.columns = columns
        self.filters = filters
        if locations is None:
            self.locations = [
                location.guid for location in Settings().locations]

    def get_list(self):
        self.view.filters += self.filters
        response = GetInventoryItems(
            self.api_session, view=self.view, locations=self.locations)
        return InventoryList(response)

    def get_item(self):
        inventory_list = self.get_list()
        if len(inventory_list) == 1:
            return inventory_list[0]
        raise ValueError
