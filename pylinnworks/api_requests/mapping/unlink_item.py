import json

from pylinnworks.api_requests.request import Request


class UnLinkItem(Request):
    url_extension = 'api/ChannelMapping/UnLinkItem'

    def __init__(
            self, api_session, inventory_item_id, channel_item_sku,
            channel_reference_id, channel_id, source, sub_source, keyword=1,
            page=1, show_linked=True, show_on_page=50, show_unlinked=True):
        self.inventoryItemId = inventory_item_id
        self.channel_item_sku = channel_item_sku
        self.channel_reference_id = channel_reference_id
        self.channel_id = channel_id
        self.source = source
        self.sub_source = sub_source
        self.keyword = keyword
        self.page = page
        self.show_linked = show_linked
        self.show_on_page = show_on_page
        self.show_unlinked = show_unlinked
        super().__init__(api_session)

    def get_data(self):
        data = {
            'inventoryItemId': self.inventoryItemId,
            'channelItemSku': self.channel_item_sku,
            'channelReferenceId': self.channel_reference_id,
            'channelOptions': json.dumps({
                'ChannelId': self.channel_id,
                'Source': self.source,
                'SubSource': self.sub_source,
                'ShowLinked': self.show_linked,
                'ShowOnPage': self.show_on_page,
                'ShowUnlinked': self.show_unlinked,
                'Source': self.source,
                'SubSource': self.sub_source
            })
        }

        self.data = data
        return data
