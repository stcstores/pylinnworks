from inventory_item import InventoryItem as InventoryItem

class Inventory():


    def __init__(self, item_list):
        self.item_list = item_list

        self.items = []
        for item in item_list:
            self.items.append(InventoryItem(item))
