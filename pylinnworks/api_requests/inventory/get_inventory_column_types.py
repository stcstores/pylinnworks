"""Requests list of column types """

from pylinnworks.api_requests.request import Request


class GetInventoryColumnTypes(Request):
    url_extension = '/api/Inventory/GetInventoryColumnTypes'

    def test_response(self, response):
        assert isinstance(response.json(), list), \
            "Error message recieved: " + response.text
        return super().test_response(response)
