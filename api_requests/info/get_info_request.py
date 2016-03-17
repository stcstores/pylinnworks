"""Requests category information"""

from .. request import Request


class GetInfoRequest(Request):
    url_extension = ''
    info = []
    name_field = ''
    id_field = ''
    default = '00000000-0000-0000-0000-000000000000'

    def __init__(self, api_session):
        super().__init__(api_session)

    def test_response(self, response):
        assert isinstance(response.json(), list),\
            response.text + " is not valid json"
        return super().test_response(response)

    def process_response(self, response):
        self.info = self.get_info()
        self.names = self.get_names()
        self.ids = self.get_ids()

    def get_info(self):
        """Return information as dict."""
        info = []
        for info_field in self.response_dict:
            new_info_dict = {}
            new_info_dict['name'] = info_field[self.name_field]
            new_info_dict['id'] = info_field[self.id_field]
            info.append(new_info_dict)
        return info

    def get_names(self):
        """Return Info names as list."""
        names = []
        for entry in self.info:
            names.append(entry['name'])
        return names

    def get_ids(self):
        """Return Info IDs as list."""
        ids = []
        for entry in self.info:
            ids.append(entry['id'])
        return ids

    def id_lookup(self, name):
        """Get id for name"""
        for entry in self.info:
            if entry['name'] == name:
                return entry['id']
        raise ValueError(_name + " Not in Names")

    def name_lookup(self, _id):
        """Get  id for _id"""
        for entry in self.info:
            if entry['id'] == _id:
                return entry['name']
        raise ValueError(_id + " Not in ids")
