"""Request inventory views. """

from .. request import Request
from . inventory_view import InventoryView


class GetInventoryViews(Request):
    url_extension = '/api/Inventory/GetInventoryViews'
    view_dicts = []
    views = []

    def __init__(self, api, start=0, count=0, view=None):
        super().__init__(api)
        for view in self.json:
            self.view_dicts.append(view)
            new_view = InventoryView()
            new_view.load_from_dict(view)
            self.views.append(new_view)

    def __iter__(self):
        for view in self.views:
            yield view

    def __getitem__(self, index):
        return self.views[index]
