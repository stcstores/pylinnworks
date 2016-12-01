from . get_channel_items import GetChannelItems


class LinkItem(GetChannelItems):
    url_extension = 'api/ChannelMapping/LinkItem'

    def __init__(
            self, api_session, channel_id, source, sub_source, keyword="",
            show_incompatible=True, show_on_page=50, show_unlinked=True,
            show_linked=True, page=1, inventory_item_id=None,
            channel_item_sku=None, channel_reference_id=None):
        self.inventory_item_id = inventory_item_id
        self.channel_item_sku = channel_item_sku
        self.channel_reference_id = channel_reference_id
        super().__init__(
            api_session, channel_id, source, sub_source, keyword="",
            show_incompatible=True, show_on_page=50, show_unlinked=True,
            show_linked=True, page=1)

    def get_data(self):
        data = super().get_data()
        data['inventoryItemId'] = self.inventory_item_id
        data['channelItemSku'] = self.channel_item_sku
        self.data = data
        return data

    def process_response(self, response):
        self.order_json = self.json
        self.order_dict = self.response_dict
