from .. pylinnworks import PyLinnworks
from .. settings . channels import Channels
from . channel_linking import ChannelLinking


class Linking(PyLinnworks):
    def __init__(self, api_session=None):
        self.api_session = api_session
        self.channels = Channels(self)
        self.linking = {
            channel.channel_id: ChannelLinking(
                self, channel) for channel
            in self.channels}

    def __repr__(self):
        return 'Linking Object'
