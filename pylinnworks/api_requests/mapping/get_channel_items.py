"""Gets channel items for channel """
import json

from pylinnworks.api_requests.request import Request


class GetChannelItems(Request):
    url_extension = 'api/ChannelMapping/GetChannelItems'

    def __init__(
            self, api_session, channel_id, source, sub_source, keyword="",
            show_incompatible=True, show_on_page=50, show_unlinked=True,
            show_linked=True, page=1):
        self.channel_id = channel_id
        self.source = source
        self.sub_source = sub_source
        self.keyword = keyword
        self.show_incompatible = show_incompatible
        self.show_on_page = show_on_page
        self.show_unlinked = show_unlinked
        self.show_linked = show_linked
        self.page = page
        super().__init__(api_session)

    def get_data(self):
        data = {
            'channelOptions': json.dumps({
                'ChannelId': self.channel_id,
                'Source': self.source,
                'SubSource': self.sub_source,
                'Keyword': self.keyword,
                'ShowIncompatible': self.show_incompatible,
                'ShowOnPage': self.show_on_page,
                'ShowUnlinked': self.show_unlinked,
                'ShowLinked': self.show_linked,
                'Page': self.page
            })
        }
        self.data = data
        return data

    def process_response(self, response):
        self.order_json = self.json
        self.order_dict = self.response_dict
