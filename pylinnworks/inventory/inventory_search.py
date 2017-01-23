from .. settings import Settings
from . inventory_view import InventoryView
from . inventory_view_filter import InventoryViewFilter
from . inventory_view_column import InventoryViewColumns
from .. api_requests import GetInventoryItems
from . inventory_list import InventoryList
from . inventory_item import InventoryItem


class InventorySearch:

    def __init__(self, api_session, filters=[], locations=None, columns=None):
        self.api_session = api_session
        self.view = InventoryView()
        if columns is None:
            self.columns = InventoryViewColumns(self.api_session).all()
        else:
            self.columns = columns
        self.filters = filters
        if locations is None:
            self.locations = [
                location.guid for location in Settings().locations]
        self.view.filters = self.filters
        self.view.columns = self.columns

    def request_page(self, start=1, count=500):
        response = GetInventoryItems(
            self.api_session, view=self.view, locations=self.locations,
            start=start, count=count)
        return response.response_dict

    def request_all(self, count=500):
        first_response = self.request_page(1, count)
        items = first_response['Items']
        total_items = first_response['TotalItems']
        start = count + 1
        while len(items) < total_items:
            response = self.request_page(start=start, count=count)
            items += response['Items']
            start += count
        return items

    def count_items(self):
        return self.request_page(count=1)['TotalItems']

    def get_items(self):
        inventory_items = [InventoryItem(
            self.api_session, data['Id']) for data in self.request_all()]
        return InventoryList(self.api_session, items=inventory_items)

    def get_item(self):
        inventory_list = self.get_items()
        if len(inventory_list) == 1:
            return InventoryItem(self.api_session, inventory_list[0]['Id'])
        raise ValueError
