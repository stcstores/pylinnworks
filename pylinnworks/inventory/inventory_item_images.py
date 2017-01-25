"""InventoryItemImages class."""

import pylinnworks.api_requests as api_requests
from . inventory_item_image import InventoryItemImage


class InventoryItemImages:
    """Container for images for inventory items.

    Allows images for inventory items to be found, added and removed.
    Attributes:
        api_session (:class: `PyLinnworks`): Login information for
            linnworks.net API.
        stock_id (int): Stock ID (GUID) for the item to which these images
            belong.
        primary (:obj: `InventoryItemImage`): The primary image for this
            inventory item.
        images (:obj: `list(InventoryItemImage)`): *list* containing the
            images for this inventory item.

    """

    def __init__(self, api_session, stock_id):
        """Initialize InventoryItemImage.

        Args:
            api_session (:class: `PyLinnworks`): Login information for
                linnworks.net API.
            stock_id (int): Stock ID (GUID) for the item to which these images
                belong.

        """
        self.api_session = api_session
        self.stock_id = stock_id
        self.images = []
        self.primary = None
        self.refresh()

    def __getitem__(self, key):
        if key in self.image_id_lookup:
            return self.images[self.image_id_lookup[key]]
        else:
            return self.images[key]

    def __len__(self):
        return len(self.images)

    def __repr__(self):
        return '{} images for item {}'.format(len(self), self.stock_id)

    def __add__(self, other):
        if isinstance(other, InventoryItemImage):
            self.images.append(other)
        elif isinstance(other, list):
            self.images += other
        elif isinstance(other, type(self)):
            self.images += other.images
        raise TypeError(
            'Operand type must be list, InventoryItemImage or'
            ' InventoryItemImages')

    def refresh(self):
        """Refresh image data from Linnworks API."""
        images = []
        image_data = self._get_images_data()
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

    def append(self, image):
        """Add image to image list.

        Args:
            image (:obj: `pylinnworks.inventory.InventoryItemImage`): Image to
                append.
        """
        self.images.append(image)

    def add(self, filepath):
        """Add image to item.

        Arguments:
            filepath (str): Path to image to be uploaded.
        """
        upload_request = api_requests.UploadFile(
            self.api_session, filepath, file_type='Image', expire_in=24)
        upload_response = upload_request.response_dict
        image_guid = upload_response[0]['FileId']
        api_requests.UploadImagesToInventoryItem(
            self.api_session, self.inventory_item.stock_id, [image_guid])

    def _get_images_data(self):
        request = api_requests.GetInventoryItemImages(
            self.api_session, self.stock_id)
        return request.response_dict
