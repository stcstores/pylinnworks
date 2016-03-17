"""Requests check to see if passed string has been used as a product SKU """

from . request import Request


class SKUExists(Request):
    url_extension = '/api/Stock/SKUExists'

    def __init__(self, api_session, sku):
        self.sku = sku
        super().__init__(api_session)

    def get_data(self):
        self.data = {
            'SKU': self.sku
        }
        return self.data
