"""InventoryItemImages class."""

import pylinnworks.api_requests as api_requests
from . inventory_item_image import InventoryItemImage


class InventoryItemImages:
    """Container for images for inventory items."""

    def __init__(self, api_session, stock_id):
        self.api_session = api_session
        self.stock_id = stock_id
        self.primary = None
        self.image_ids = []
        self.image_id_lookup = {}
        self.refresh()

    def get_images_data(self):
        request = api_requests.GetInventoryItemImages(
            self.api_session, self.stock_id)
        return request.response_dict

    def refresh(self):
        images = []
        image_data = self.get_images_data()
        for image in image_data:
            images.append(InventoryItemImage(
                self.api_session, image['pkRowId'], self.stock_id,
                image['Source'], image['IsMain']))
        for image in images:
            self.image_ids.append(image.image_id)
            self.image_id_lookup[image.image_id] = image
            if image.primary:
                self.primary = image
        self.images = images
        return images

    def __getitem__(self, key):
        if key in self.image_id_lookup:
            return self.images[self.image_id_lookup[key]]
        else:
            return self.images[key]

    def __len__(self):
        return len(self.images)

    def __repr__(self):
        return '{} images for item {}'.format(len(self), self.stock_id)

    def append(self, image):
        self.images.append(image)
        self.update()

    def extend(self, images):
        for image in images:
            self.append(image)
        self.update()

    def add(self, filepath):
        """Add image to item.

        Arguments:
            filepath -- Path to image to be uploaded.
        """
        upload_request = api_requests.UploadFile(
            self.api_session, filepath, file_type='Image', expire_in=24)
        upload_response = upload_request.response_dict
        image_guid = upload_response[0]['FileId']
        return api_requests.UploadImagesToInventoryItem(
            self.api_session, self.inventory_item.stock_id, [image_guid])
