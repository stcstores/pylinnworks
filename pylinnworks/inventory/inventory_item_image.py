"""Contains InventoryItemImage class."""

import os
import webbrowser
from mimetypes import guess_extension
import requests

import pylinnworks.api_requests as api_requests


class InventoryItemImage:
    """Container for images for Inventory Items.

    Allows inventory item images to be viewed, saved and deleted.

    Attributes:
        api_session (pylinnworks.PyLinnworks): API session object.
        image_id (str): Image ID (GUID).
        stock_id (str): Stock ID (GUID) for inventory item to which this image
            belongs.
        primary (bool): True if this is the primary image for the inventory
            item.
        url (str): URL at which this image can be found.
        thumb_url: URL at which the thumbnail of this image can be found.
    """

    def __init__(self, api_session, image_id, stock_id, url, primary):
        """Initialize self.

        Args:
            api_session (pylinnworks.PyLinnworks): API session and login
                details.
            image_id (str): Image ID (GUID) for image.
            stock_id (str): Stock ID (GUID) for inventory item to which this
                image belongs.
            url (str): URL at which this image can be found.
            primary (bool): True if image is the primary image for the item.
        """
        self.api_session = api_session
        self.image_id = image_id
        self.stock_id = stock_id
        self.primary = primary
        self.thumb_url = url
        self.url = self.thumb_url.replace('tumbnail_', '')

    def __repr__(self):
        return 'InventoryItemImage: {}'.format(self.image_id)

    def save(self, path):
        """Download image.

        Download this image and save it locally.

        Args:
            path (str): Filepath at which to save the image. If path is a
                directory the self.image_id will be used as a filename. The
                correct file extension will be appended to the path.

        Returns:
            Path to saved file.
        """
        if os.path.isdir(path):
            path = os.path.join(path, self.stock_id)
        return self._save_image_from_url(self.url, path=path)

    def save_thumb(self, path):
        """Download thumbnail image.

        Download a thumbnail of this image and save it locally.

        Args:
            path (str): Filepath at which to save the image. If path is a
                directory [self.image_id]_thumb will be used as a filename. The
                correct file extension will be appended to the path.

        Returns:
            Path to saved file.
        """
        if os.path.isdir(path):
            path = os.path.join(path, '{}_thumb'.format(self.stock_id))
        return self._save_image_from_url(self.thumb_url, path)

    def view(self):
        """View image in default web browser."""
        webbrowser.open(self.url)

    def view_thumb(self):
        """View thubnail image in default web browser."""
        webbrowser.open(self.thumb_url)

    def remove(self):
        """Delete this image from Linnworks."""
        request = api_requests.DeleteImageFromInventoryItem(
            self.api_session, self.thumb_url, self.stock_id)
        return request

    def _save_image_from_url(self, url, path):
        request = requests.get(url)
        path = ''.join([path, self._get_extension(request)])
        with open(path, 'wb') as image_file:
            for chunk in request:
                image_file.write(chunk)
        return path

    def _get_extension(self, request):
        extension = guess_extension(
            request.headers['content-type'].split()[0].rstrip(";"))
        if extension.lower() in ('.jpe', '.jpeg'):
            return '.jpg'
        else:
            return extension
