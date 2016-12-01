from pylinnworks.api_requests.request import Request


class GetConfig(Request):
    url_extension = 'api/ChannelIntegration/GetConfig'

    def __init__(self, api_session, channel_id):
        self.channel_id = channel_id
        super().__init__(api_session)

    def get_data(self):
        data = {'channelId': self.channel_id}
        self.data = data
        return data

    def process_response(self, response):
        self.order_json = self.json
        self.order_dict = self.response_dict
