import json

from pylinnworks.api_requests.request import Request


class GetChannelTotals(Request):
    url_extension = 'api/ChannelMapping/GetChannelTotals'

    def __init__(self, api_session, channel_id, source, sub_source):
        self.channel_id = channel_id
        self.source = source
        self.sub_source = sub_source
        super().__init__(api_session)

    def get_data(self):
        data = {
            'request': json.dumps({
                'ChannelId': self.channel_id,
                'Source': self.source,
                'SubSource': self.sub_source,
            })
        }

        self.data = data
        return data
