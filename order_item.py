from . inventory_item import InventoryItem as InventoryItem


class OrderItem:

    def __init__(self, item_data):
        self.guid = item_data['ItemId']
        self.sku = item_data['SKU']
        self.item_title = item_data['Title']
        self.department = item_data['CategoryName']

    def getInventoryItem(self, api):
        return InventoryItem(api, self.guid)
