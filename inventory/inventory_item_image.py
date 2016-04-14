import os
import shutil
import webbrowser
from mimetypes import guess_extension
import requests

from linnapi.api_requests.inventory.images.delete_image_from_inventory_item \
    import DeleteImageFromInventoryItem


class InventoryItemImage:

    def __init__(self, api_session, image_id, stock_id, url, primary):
        self.api_session = api_session
        self.image_id = image_id
        self.stock_id = stock_id
        self.primary = primary
        self.thumb_url = url
        self.url = self.thumb_url.replace('tumbnail_', '')

    def save_url_image(self, url, name=None, path=''):
        request = requests.get(url)
        ext = os.path.splitext(name)[-1].lower()
        if name is None:
            name = self.image_id + self.get_extension(request)
        if ext == '':
            name += self.get_extension(request)
        if len(path) == 0:
            path = os.getcwd()
        filepath = os.path.join(path, name)
        if request.status_code == 200:
            with open(filepath, 'wb') as image_file:
                for chunk in request:
                    image_file.write(chunk)
            return filepath
        return False

    def get_extension(self, request):
        extension = guess_extension(
            request.headers['content-type'].split()[0].rstrip(";"))
        if extension.lower() in ('.jpe', '.jpeg'):
            return '.jpg'
        else:
            return extension

    def save(self, name=None, path=''):
        return self.save_url_image(self.url, name=name, path=path)

    def save_thumb(self, name=None, path=''):
        return self.save_url_image(self.thumb_url, name=name, path=path)

    def view(self):
        webbrowser.open(self.url)

    def view_thumb(self):
        webbrowser.open(self.thumb_url)

    def remove(self):
        request = DeleteImageFromInventoryItem(
            self.api_session, self.thumb_url, self.stock_id)
        return request
