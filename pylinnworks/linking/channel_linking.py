"""ChannelLinking class.

Represents a Linnworks selling channel and provides method for interacting
with that channel and it's items.
"""

from . channel_item import ChannelItem, AmazonChannelItem, EbayChannelItem
from ..api_requests import GetChannelItems
from ..api_requests import GetChannelTotals
from ..api_requests import StatusError
from ..api_requests import ExecConfigMethod
from . linking_list import LinkingList


class ChannelLinking:
    """Encapsulates Linnworks selling channel."""

    channel_item_lookup = {
        'AMAZON': AmazonChannelItem, 'EBAY': EbayChannelItem}
    total = None
    unlinked = None
    linked = None

    def __init__(self, api_session, channel):
        """Set class attributes and gets item counts."""
        self.api_session = api_session
        self.channel = channel
        self.channel_id = channel.channel_id
        self.source = channel.source
        self.sub_source = channel.sub_source
        if self.source in self.channel_item_lookup:
            self.channel_item_type = self.channel_item_lookup[self.source]
        else:
            self.channel_item_type = ChannelItem
        self.get_totals()

    def __repr__(self):
        return 'ChannelLinking: {}'.format(self.channel)

    def __str__(self):
        return '{} {}'.format(self.source, self.sub_source)

    def __lt__(self, other):
        return self.channel_id < other.channel_id

    def get_totals(self):
        """Get current count of linked, unlinked and total items."""
        try:
            request = GetChannelTotals(
                self.api_session, self.channel_id, self.source,
                self.sub_source)
        except StatusError:
            return {}
        else:
            data = request.response_dict
            self.total = data['Total']
            self.unlinked = data['Unlinked']
            self.linked = data['Linked']
            return data

    def download_listings(self):
        """Trigger update of Linnworks list of items for this channel."""
        ExecConfigMethod(
            self.api_session, channel_id=self.channel_id, source=self.source,
            property_name='DownloadListings', function_name='DownloadListings')

    def request_channel_items(
            self, page, keyword='', show_linked=True, show_unlinked=True,
            show_on_page=50):
        """Make API request for one page of channel items.

        Makes a single request to linnworks.net API for a single page of
        channel items for this channel.

        Arguments:
            page:
                type: int
                Specify page number to be requested

        Kwargs:
            show_linked:
                type: bool
                default: True
                Include channel items that are linked to linnworks items
            show_unlinked:
                type: bool
                default: True
                Include channel items that are not linked to linnworks items

        Returns LinkingList
        """
        request = GetChannelItems(
            self.api_session, self.channel_id, self.source, self.sub_source,
            show_linked=show_linked, show_unlinked=show_unlinked, page=page,
            keyword=keyword, show_on_page=50)
        linking_list = LinkingList([self.channel_item_type(
            self.api_session, self.channel, item) for item in
            request.response_dict])
        if len(linking_list) > 0:
            return linking_list
        else:
            return LinkingList([])

    def get_items(self, keyword='', linked=True, unlinked=True):
        """Get all channel items for this channel.

        Kwargs:
            show_linked:
                type: bool
                default: True
                Include channel items that are linked to linnworks items
            show_unlinked:
                type: bool
                default: True
                Include channel items that are not linked to linnworks items

        Returns LinkingList
        """
        page = 1
        show_on_page = 50
        request_items = self.request_channel_items(
            page, show_linked=linked, show_unlinked=unlinked,
            show_on_page=show_on_page, keyword=keyword)
        items = request_items
        while len(request_items) == show_on_page:
            page += 1
            request_items = self.request_channel_items(
                page, keyword=keyword, show_linked=linked,
                show_unlinked=unlinked)
            items = items + request_items
        return items
