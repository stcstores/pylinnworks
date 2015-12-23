from . inventory_item import InventoryItem as InventoryItem


class BasicItem:

    def __init__(self):
        self.guid = None
        self.sku = None
        self.title = None
        self.purchase_price = None
        self.retail_price = None
        self.barcode = None
        self.category_id = None
        self.depth = None
        self.height = None
        self.package_group_id = None
        self.postage_service_id = None
        self.tax_rate = None
        self.variation_group_name = None
        self.weight = None
        self.width = None
        self.meta_data = None
        self.quantity = None
        self.category = None
        self.package_group = None
        self.postage_service = None

    def get_inventory_self(self, api):
        return Inventoryself(api, self.guid)
