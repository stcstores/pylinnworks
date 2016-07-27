"""Request stock level for inventory item """

from pylinnworks.api_requests.request import Request
from pylinnworks.functions import is_guid


class GetStockLevel(Request):
    url_extension = '/api/Stock/GetStockLevel'

    def __init__(self, api_session, stock_id):
        self.stock_id = stock_id
        super().__init__(api_session)

    def test_request(self):
        assert is_guid(self.stock_id), "Stock ID must be valid GUID."
        return super().test_request()

    def get_data(self):
        data = {
            'stockItemId': self.stock_id
        }
        return data

    def test_response(self, response):
        return super().test_response(response)
