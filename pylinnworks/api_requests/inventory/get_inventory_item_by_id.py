"""Returns inventory item data for the item with the specifed stock id.

Arguments:
    stock_id -- GUID of inventory item.
"""

from pylinnworks.api_requests.request import Request
from pylinnworks.functions import is_guid


class GetInventoryItemByID(Request):
    url_extension = '/api/Inventory/GetInventoryItemById'

    def __init__(self, api_session, stock_id, test=True):
        self.stock_id = stock_id
        super().__init__(api_session, test=test)

    def test_request(self):
        assert is_guid(self.stock_id), "Stock ID must be vaild GUID."
        return super().test_request()

    def get_data(self):
        data = {'id': self.stock_id}
        return data

    def test_response(self, response):
        assert isinstance(response.json(), dict), \
            "Error message recieved: " + response.text
        return super().test_response(response)
