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
        self.data = data
        return data
