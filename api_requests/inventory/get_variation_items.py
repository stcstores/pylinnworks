"""Requests list of variation item's stock_ids for given variation parent """

from .. request import Request
from .. functions import is_guid


class GetVariationItems(Request):
    url_extension = '/api/Stock/GetVariationItems'

    def __init__(self, api_session, parent_stock_id):
        self.parent_stock_id = parent_stock_id
        super().__init__(api_session)

    def test_request(self):
        assert is_guid(self.parent_stock_id), \
            "Parent Stock ID must be valid GUID."
        return super().test_request()

    def get_data(self):
        data = {'pkVariationItemId': self.parent_stock_id}
        return data

    def test_response(self, response):
        assert isinstance(response.json(), list), \
            "Error message recieved: " + response.text
        return super().test_response(response)

    def process_response(self, response):
        self.variation_children = []
        for child in self.response_dict:
            self.variation_children.append(child['pkStockItemId'])
