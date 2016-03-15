"""Request inventory views. """

from .. request import Request
from . inventory_view import InventoryView
from . inventory_view_column import InventoryViewColumn


class GetInventoryViews(Request):
    url_extension = '/api/Inventory/GetInventoryViews'
    view_dicts = []
    views = []
    standard_columns = [
        InventoryViewColumn(
            column_name='SKU', display_name='SKU'
        ),
        InventoryViewColumn(
            column_name='Title', display_name='Title'
        ),
        InventoryViewColumn(
            column_name='RetailPrice', display_name='Retail', field='Double'
        ),
        InventoryViewColumn(
            column_name='PurchasePrice', display_name='Purchase',
            field='Double'
        ),
        InventoryViewColumn(
            column_name='Available', display_name='Available', field='Int'
        ),
        InventoryViewColumn(
            column_name='StockLevel', display_name='Level', field='Int'
        )
    ]

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
