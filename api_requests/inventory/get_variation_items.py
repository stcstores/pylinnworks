"""Requests list of variation item's stock_ids for given variation parent """

from .. request import Request


class GetVariationItems(Request):
    url_extension = '/api/Stock/GetVariationItems'

    def __init__(self, api_session, parent_stock_id):
        self.parent_stock_id = parent_stock_id
        super().__init__(api_session)

    def get_data(self):
        data = {'pkVariationItemId': self.parent_stock_id}
        self.data = data
        return data

    def process_response(self, response):
        self.variation_children = []
        for child in self.response_dict:
            self.variation_children.append(child['pkStockItemId'])
