from linnapi.api_requests.inventory.get_variation_items \
    import GetVariationItems
from . variation_inventory_item import VariationInventoryItem


class VariationGroup():
    def __init__(self, api_session, stock_id, sku, title, children=[]):
        self.api_session = api_session
        self.stock_id = stock_id
        self.sku = sku
        self.title = title
        self.children = children

    def get_children(self):
        request = GetVariationItems(self.api_session, self.stock_id)
        return request.response_dict
