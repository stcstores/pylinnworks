"""Requests channel prices for item """

from pylinnworks.api_requests.request import Request
from pylinnworks.functions import is_guid


class GetInventoryItemPrices(Request):
    url_extension = '/api/Inventory/GetInventoryItemPrices'

    def __init__(self, api_session, stock_id):
        self.stock_id = stock_id
        super().__init__(api_session)

    def test_request(self):
        assert is_guid(self.stock_id), "Stock ID must be valid GUID."
        return super().test_request()

    def get_data(self):
        data = {
            'inventoryItemId': self.stock_id
        }
        return data

    def test_response(self, response):
        assert isinstance(response.json(), list), \
            "Error message recieved: " + response.text
        return super().test_response(response)
