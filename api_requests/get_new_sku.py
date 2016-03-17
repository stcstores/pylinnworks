"""Requests an unused product SKU """

from . request import Request


class GetNewSKU(Request):
    url_extension = '/api/Stock/GetNewSKU'

    def process_response(self, response):
        self.sku = self.response_dict
