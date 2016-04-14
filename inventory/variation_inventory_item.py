from . inventory_item import InventoryItem


class VariationInventoryItem(InventoryItem):

    def __init__(self, api_session, stock_id, sku, title):
        super().__init__(api_session, stock_id, sku, title)
