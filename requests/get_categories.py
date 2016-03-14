"""Requests category information"""

from . request import Request


class GetCategories(Request):
    url_extension = '/api/Inventory/GetCategories'
    info = []

    def __init__(self, api):
        super().__init__(api)
        self.execute()

    def process_response(self, response):
        self.info = self.get_info()
        self.names = self.get_names()
        self.ids = self.get_ids()

    def get_info(self):
        """Return category information as dict."""
        info = []
        for category in self.response.json():
            new_category = {}
            new_category['name'] = category['CategoryName']
            new_category['id'] = category['CategoryId']
            info.append(new_category)
        return info

    def get_names(self):
        """Return category names as list."""
        category_names = []
        for category in self.info:
            category_names.append(category['name'])
        return category_names

    def get_ids(self):
        """Return category IDs as list."""
        category_ids = []
        for category in self.info:
            category_ids.append(category['id'])
        return category_ids

    def id_lookup(self, category_name):
        for category in self.info:
            if category['name'] == category_name:
                return category['id']
        raise ValueError(category_name + " Not in Categorys")

    def name_lookup(self, category_id):
        for category in self.info:
            if category['id'] == category_id:
                return category['name']
        raise ValueError(category_name + " Not in Categorys")
