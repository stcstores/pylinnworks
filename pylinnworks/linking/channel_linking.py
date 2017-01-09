from . channel_item import ChannelItem, AmazonChannelItem, EbayChannelItem
from ..api_requests import GetChannelItems
from ..api_requests import GetChannelTotals
from ..api_requests import StatusError
from . linking_list import LinkingList


class ChannelLinking:
    channel_item_lookup = {
        'AMAZON': AmazonChannelItem, 'EBAY': EbayChannelItem}
    total = None
    unlinked = None
    linked = None

    def __init__(self, api_session, channel):
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

    def get_totals(self):
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

    def request_channel_items(
            self, page, show_linked=True, show_unlinked=True):
        request = GetChannelItems(
            self.api_session, self.channel_id, self.source, self.sub_source,
            show_linked=show_linked, show_unlinked=show_unlinked, page=page)
        linking_list = LinkingList([self.channel_item_type(
            self.api_session, self.channel, item) for item in
            request.response_dict])
        if len(linking_list) > 0:
            return linking_list
        else:
            return LinkingList([])

    def get_all(self, show_linked=True, show_unlinked=True):
        page = 1
        request_items = self.request_channel_items(
            page, show_linked, show_unlinked)
        items = request_items
        while len(request_items) > 0:
            page += 1
            request_items = self.request_channel_items(
                page, show_linked, show_unlinked)
            items = items + request_items
        return items
