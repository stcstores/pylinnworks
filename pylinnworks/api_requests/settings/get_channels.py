from linnapi.api_requests.request import Request


class GetChannels(Request):
    url_extension = '/api/Inventory/GetChannels'

    def test_response(self, response):
        assert isinstance(response.json(), list),\
            response.text + " is not valid json"
        return super().test_response(response)
