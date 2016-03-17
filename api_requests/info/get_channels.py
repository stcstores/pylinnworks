from .. request import Request
from ... channel import Channel


class GetChannels(Request):
    url_extension = '/api/Inventory/GetChannels'

    def process_response(self, response):
        self.sources = []
        self.source_types = []
        self.sub_sources = []
        self.channels = []
        for channel in self.response_dict:
            self.sources.append(channel['Source'])
            self.source_types.append(channel['SourceType'])
            self.sub_sources.append(channel['SubSource'])
            self.channels.append(Channel(channel))

    def test_response(self, response):
        assert isinstance(response.json(), list),\
            response.text + " is not valid json"
        return super().test_response(response)
