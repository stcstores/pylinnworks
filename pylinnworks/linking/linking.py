"""Linking class for interacting with channel linking."""

from .. pylinnworks import PyLinnworks
from .. settings . channels import Channels
from . channel_linking import ChannelLinking


class Linking(PyLinnworks):
    """Provide methods for working with channel linking."""

    def __init__(self, api_session=None, source=None, sub_source=None):
        """Set attributes and download selling channel information."""
        self.api_session = api_session
        self.channels = Channels(self)
        self.source = source
        self.sub_source = sub_source
        self.get_linking()

    def get_linking(self):
        """Download selling channel information."""
        self.linking = []
        for channel in self.channels:
            if self.source is not None and channel.source != self.source:
                continue
            if self.sub_source is not None and \
                    channel.sub_source != self.sub_source:
                continue
            self.linking.append(ChannelLinking(self, channel))
        self.linking = sorted(self.linking)

    @classmethod
    def get_channel_by_ID(cls, channel_id):
        """Get channel by channel ID."""
        channels = Channels(cls)
        for channel in channels:
            if channel.channel_id == channel_id:
                return ChannelLinking(cls, channel)
        raise IndexError('Channel ID non existant')

    @classmethod
    def get_channel_by_sub_source(cls, sub_source):
        """Get channel by channel Sub Source."""
        channels = Channels(cls)
        for channel in channels:
            if channel.sub_source == sub_source:
                return ChannelLinking(cls, channel)
        raise IndexError('Sub Source non existant')

    def __iter__(self):
        for channel in self.linking:
            yield channel

    def __getitem__(self, index):
        return self.linking[index]

    def __repr__(self):
        return 'Linnworks Linking'

    def __len(self):
        return len(self.linking)
