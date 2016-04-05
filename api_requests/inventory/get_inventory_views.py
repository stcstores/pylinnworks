"""Request inventory views. """

from linnapi.api_requests.request import Request
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

    def process_response(self, response):
        for view in self.response_dict:
            self.view_dicts.append(view)
            new_view = InventoryView()
            new_view.load_from_dict(view)
            self.views.append(new_view)

    def __iter__(self):
        for view in self.views:
            yield view

    def __getitem__(self, index):
        return self.views[index]

    def test_response(self, response):
        assert isinstance(response.json(), list), \
            "Error message recieved: " + response.text
        return super().test_response(response)
