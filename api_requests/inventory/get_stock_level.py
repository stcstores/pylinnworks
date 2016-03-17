"""Request stock level for inventory item """

from .. request import Request


class GetStockLevel(Request):
    url_extension = '/api/Stock/GetStockLevel'

    def __init__(self, api_session, stock_id):
        self.stock_id = stock_id
        super().__init__(api_session)

    def get_data(self):
        data = {
            'stockItemId': self.stock_id
        }
        return data

    def test_response(self, response):
        assert isinstance(response.json(), int), \
            "Error message recieved: " + response.text
        return super().test_response(response)
