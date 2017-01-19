"""Includes ChannelItem class for encapsulating Linnworks Channel items.

Provides methods for manipulating Linnworks channel items.
"""

from .. api_requests import LinkItem
from .. api_requests import UnLinkItem


class ChannelItem:
    """Encapsulates items from selling channels.

    Provides methods for interacting with items from selling channels.
    """

    def __init__(self, api_session, channel, data):
        """Set object attributes from API response."""
        self.api_session = api_session
        self.channel = channel
        self.source = channel.source
        self.sub_source = channel.sub_source
        self.channel_id = channel.channel_id
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
        self.load_additional(data)

    def load_additional(self, data):
        """Add additional object attributes from API response."""
        pass

    def __repr__(self):
        string = 'ChannelItem: From: {} with SKU: {}'.format(
            self.channel, self.channel_reference_id)
        if self.is_linked:
            string + ' Linked to: {}'.format(self.linked_item_sku)
        return string

    def link(self, inventory_item_id):
        """Link this item to the inventory item with given stock ID (GUID)."""
        LinkItem(
            self.api_session, self.channel.channel_id, self.channel.source,
            self.channel.sub_source, show_linked=False,
            inventory_item_id=inventory_item_id, channel_item_sku=self.sku,
            channel_reference_id=self.channel_reference_id)

    def unlink(self):
        """Remove link between this item and any inventory item."""
        UnLinkItem(
            self.api_session, self.linked_item_id, self.sku,
            self.channel_reference_id, self.channel.channel_id,
            self.channel.source, self.channel.sub_source)


class AmazonChannelItem(ChannelItem):
    """Encapsulates channel items from Amazon."""

    def load_additional(self, data):
        """Add additional object attributes from API response."""
        self.fba = data['FBA']


class EbayChannelItem(ChannelItem):
    """Encapsulates channel items from eBay."""

    def load_additional(self, data):
        """Add additional object attributes from API response."""
        self.item_number = data['ItemNumber']
        self.mapped_by = data['MappedBy']
        self.relist_pending = data['RelistPending']
