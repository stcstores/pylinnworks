from linnapi.api_requests.request import Request


class DeleteImageFromInventoryItem(Request):
    url_extension = '/api/Inventory/DeleteImagesFromInventoryItem'

    def __init__(self, api_session, image_url, stock_id):
        self.image_url = image_url
        self.stock_id = stock_id
        super().__init__(api_session)

    def test_request(self):
        return super().test_request()

    def get_data(self):
        data = {'imageURL': self.image_url, 'inventoryItemId': self.stock_id}
        return data

    def test_response(self, response):
        return super().test_response(response)
