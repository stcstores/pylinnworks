from . inventory_item import InventoryItem as InventoryItem

from . lstools . table import Table as Table

class Inventory():


    def __init__(self, item_list, api):
        self.item_list = item_list
        self.api = api
        self.get_info()
        self.load_items()
        
    def __getitem__(self, item_number):
        return self.items[item_number]
    
    def __iter__(self):
        for item in self.items:
            yield item
    
    
    def get_info(self):
        self.extended_properties = self.api.get_extended_property_names()
        self.category_lookup = self.get_category_lookup()
        self.postage_group_lookup = self.get_postage_group_lookup()
        self.postal_service_lookup = self.get_postal_service_lookup()
        
    def load_items(self):
        self.items = []
        i = 1
        for item in self.item_list:
            self.items.append(InventoryItem(item, self))
            #print(str(i) + ' / ' + str(len(item_list)))
            i += 1
            
    def get_category_lookup(self):
        category_info = self.api.get_category_info()
        category_lookup = {}
        for category in category_info:
            category_lookup[category['id']] = category['name']
        return category_lookup
    
    def get_postage_group_lookup(self):
        postage_info = self.api.get_packaging_group_info()
        postage_group_lookup = {}
        for group in postage_info:
            postage_group_lookup[group['id']] = group['name']
        return postage_group_lookup
    
    def get_postal_service_lookup(self):
        postal_info = self.api.get_shipping_method_info()
        postal_service_lookup = {}
        for service in postal_info:
            postal_service_lookup[service['id']] = service['name']
        return postal_service_lookup


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
