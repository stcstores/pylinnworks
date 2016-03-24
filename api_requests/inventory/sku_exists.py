"""Requests check to see if passed string has been used as a product SKU """

from linnapi.api_requests.request import Request


class SKUExists(Request):
    url_extension = '/api/Stock/SKUExists'

    def __init__(self, api_session, sku):
        self.sku = sku
        super().__init__(api_session)

    def get_data(self):
        data = {
            'SKU': self.sku
        }
        return data

    def test_request(self):
        assert isinstance(self.sku, str), 'sku must be string'
        return super().test_request()

    def test_response(self, response):
        assert response.text in ('true', 'false'), \
            response.text + " is an invalid response"
        return super().test_response(response)
