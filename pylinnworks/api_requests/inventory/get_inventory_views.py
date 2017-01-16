"""Request inventory views. """

from pylinnworks.api_requests.request import Request


class GetInventoryViews(Request):
    url_extension = '/api/Inventory/GetInventoryViews'

    def __iter__(self):
        for view in self.views:
            yield view

    def __getitem__(self, index):
        return self.views[index]

    def test_response(self, response):
        assert isinstance(response.json(), list), \
            "Error message recieved: " + response.text
        return super().test_response(response)
