from .. request import Request


class ExecConfigMethod(Request):

    url_extension = 'api/ChannelIntegration/ExecConfigMethod'

    def __init__(
            self, api_session, channel_id=None, source=None,
            property_name=None, function_name=None):
        self.api_session = api_session
        self.channel_id = channel_id
        self.source = source
        self.property_name = property_name
        self.function_name = function_name
        super().__init__(api_session)

    def get_data(self):
        data = {
            'channelId': self.channel_id,
            'source': self.source,
            'propertyName': self.property_name,
            'functionName': self.function_name
        }
        self.data = data
        return data
