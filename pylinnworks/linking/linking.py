from .. settings . channels import Channels
from . channel_linking import ChannelLinking


class Linking:
    def __init__(self, api_session=None):
        self.api_session = api_session
        self.channels = Channels(self.api_session)
        self.linking = {
            channel.channel_id: ChannelLinking(
                self.api_session, channel) for channel
            in self.channels}

    def __repr__(self):
        return 'Linking Object'
