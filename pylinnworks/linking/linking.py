from .. pylinnworks import PyLinnworks
from .. settings . channels import Channels
from . channel_linking import ChannelLinking


class Linking(PyLinnworks):
    def __init__(self, api_session=None, source=None, sub_source=None):
        self.api_session = api_session
        self.channels = Channels(self)
        self.source = source
        self.sub_source = sub_source
        self.get_linking()

    def get_linking(self):
        self.linking = []
        for channel in self.channels:
            if self.source is not None and channel.source != self.source:
                continue
            if self.sub_source is not None and \
                    channel.sub_source != self.sub_source:
                continue
            self.linking.append(ChannelLinking(self, channel))
        self.linking = sorted(self.linking)

    def __iter__(self):
        for channel in self.linking:
            yield channel

    def __getitem__(self, index):
        return self.linking[index]

    def __repr__(self):
        return 'Linnworks Linking'

    def __len(self):
        return len(self.linking)
