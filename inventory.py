from inventory_item import InventoryItem as InventoryItem

from lstools . table import Table as Table

class Inventory():


    def __init__(self, item_list):
        self.item_list = item_list

        self.items = []
        for item in item_list:
            self.items.append(InventoryItem(item))

    def to_table(self):
        header = ['SKU', 'Title', 'Purchase Price', 'Retail Price', 'Barcode']
        table_array = []
        for item in self.items:
            new_row = []
            new_row.append(item.sku)
            new_row.append(item.title)
            new_row.append(item.purchase_price)
            new_row.append(item.retail_price)
            new_row.append(item.barcode)
            table_array.append(new_row)
        table = Table()
        table.load_from_array(table_array, header)
        return table
