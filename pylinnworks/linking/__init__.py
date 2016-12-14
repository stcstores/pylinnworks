from .. linnworks_api_session import LinnworksAPISession
from ..api_requests import GetChannelItems
from .. settings . channels import Channels


class Linking:
    def __init__(self, api_session=None):
        if api_session is None:
            self.api_session = LinnworksAPISession()
        else:
            self.api_session = api_session
        self.channels = Channels(self.api_session)
        self.linking = {
            channel.channel_id: ChannelLinking(
                self.api_session, channel) for channel
            in self.channels}


class ChannelItem:
    def __init__(self, api_session, channel, data):
        self.channel_reference_id = data['ChannelReferenceId']
        self.end_when_stock = data['EndWhenStock']
        self.ignore_sync = data['IgnoreSync']
        self.is_linked = data['IsLinked']
        self.is_match_by_title = data['IsMatchByTitle']
        self.is_suggested_to_link = data['IsSuggestedToLink']
        self.linked_item_id = data['LinkedItemId']
        self.linked_item_sku = data['LinkedItemSku']
        self.linked_item_title = data['LinkedItemTitle']
        self.max_listed_quantity = data['MaxListedQuantity']
        self.quantity = data['Quantity']
        self.sku = data['SKU']
        self.stock_percentage = data['StockPercentage']
        self.title = data['Title']


class AmazonChannelItem(ChannelItem):
    def __init__(self, api_session, data):
        self.fba = data['FBA']
        super().__init__(api_session, data)


class EbayChannelItem(ChannelItem):
    def __init__(self, api_session, data):
        self.item_number = data['ItemNumber']
        self.mapped_by = data['MappedBy']
        self.relist_pending = data['RelistPending']
        super().__init(api_session, data)


class LinkingList:
    def __init__(self, items):
        self.items = items

    def __getitem__(self, index):
        return self.items[index]

    def __len__(self):
        return len(self.items)

    def __add__(self, other):
        if isinstance(other, LinkingList):
            self.items += other
        else:
            raise TypeError

    def linked(self):
        return LinkingList([item for item in self.items if item.is_linked])

    def unlinked(self):
        return LinkingList([item for item in self.items if not item.is_linked])

    def get_item_by_channel_sku(self, sku):
        for item in self.items:
            if item.sku == sku:
                return item
        raise ValueError

    def get_item_by_linked_sku(self, sku):
        for item in self.items:
            if item.linked_sku == sku:
                return item
        raise ValueError


class ChannelLinking:
    channel_item_lookup = {
        'AMAZON': AmazonChannelItem, 'EBAY': EbayChannelItem}

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

    def __str__(self):
        return str(self.channel)

    def request_channel_items(
            self, page, show_linked=True, show_unlinked=True):
        request = GetChannelItems(
            self.api_session, self.channel_id, self.source, self.sub_source,
            show_linked=show_linked, show_unlinked=show_unlinked, page=page)
        return LinkingList([self.channel_item_type(
            self.api_session, self.channel, item) for item in
            request.response_dict])

    def get_all(self, show_linked=True, show_unlinked=True):
        page = 1
        request_items = self.request_channel_items(
            page, show_linked, show_unlinked)
        items = request_items
        while len(request_items) > 0:
            page += 1
            request_items = request_items = self.request_channel_items(
                page, show_linked, show_unlinked)
            items += request_items
        return items
