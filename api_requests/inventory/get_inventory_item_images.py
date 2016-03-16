"""Requests image urls for inventory item """

from .. request import Request


class GetInventoryItemImages(Request):
    url_extension = '/api/Inventory/GetInventoryItemImages'

    def __init__(self, api, stock_id):
        self.stock_id = stock_id
        super().__init__(api)

    def get_data(self):
        data = {'inventoryItemId': self.stock_id}
        self.data = data
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
