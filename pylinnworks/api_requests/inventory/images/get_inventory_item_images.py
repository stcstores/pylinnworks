"""Requests image urls for inventory item """

from pylinnworks.api_requests.request import Request


class GetInventoryItemImages(Request):
    url_extension = '/api/Inventory/GetInventoryItemImages'

    def __init__(self, api_session, stock_id):
        self.stock_id = stock_id
        super().__init__(api_session)

    def get_data(self):
        data = {'inventoryItemId': self.stock_id}
        return data

    def process_response(self, response):
        self.images = []
        for image in self.response_dict:
            if image['IsMain'] is True:
                image_url = image['Source'].replace('tumbnail_', '')
                self.images.append(image_url)
        for image in self.response_dict:
            if image['IsMain'] is not True:
                image_url = image['Source'].replace('tumbnail_', '')
                self.images.append(image_url)

    def test_response(self, response):
        assert isinstance(response.json(), list), \
            "Error message recieved: " + response.text
        return super().test_response(response)
