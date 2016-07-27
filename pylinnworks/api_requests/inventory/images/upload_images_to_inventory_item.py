import json

from pylinnworks.api_requests.request import Request


class UploadImagesToInventoryItem(Request):
    url_extension = '/api/Inventory/UploadImagesToInventoryItem'

    def __init__(self, api_session, stock_id, image_ids):
        self.stock_id = stock_id
        self.image_ids = image_ids
        super().__init__(api_session)

    def test_request(self):
        assert(isinstance(self.image_ids, list))
        assert(len(self.image_ids) > 0)
        return super().test_request()

    def get_data(self):
        data = {
            'inventoryItemId': self.stock_id,
            'imageIds': json.dumps(self.image_ids)}
        return data

    def test_response(self, response):
        return super().test_response(response)
