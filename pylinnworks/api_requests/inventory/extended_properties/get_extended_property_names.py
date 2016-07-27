"""Requests extended property names """

from pylinnworks.api_requests.request import Request


class GetExtendedPropertyNames(Request):
    url_extension = '/api/Inventory/GetExtendedPropertyNames'

    def test_response(self, response):
        assert isinstance(response.json(), list), \
            "Error message recieved: " + response.text
        return super().test_response(response)
