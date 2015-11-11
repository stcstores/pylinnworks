from . inventory_item import InventoryItem as InventoryItem

from lstools import Table as Table


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
        self.package_group_lookup = self.get_package_group_lookup()
        self.postal_service_lookup = self.get_postal_service_lookup()

    def load_items(self):
        self.items = []
        for item in self.item_list:
            new_inv_item = InventoryItem(self.api, item['Id'])
            new_inv_item.load_from_json(item, self)
            self.items.append(new_inv_item)

    def get_inventory_item_details(self):
        for item in self.items:
            request = self.api.get_inventory_item_by_id(item.stock_id)
            item.category_id = request['CategoryId']
            item.category = self.category_lookup[item.category_id]
            item.depth = request['Depth']
            item.height = request['Height']
            item.package_group_id = request['PackageGroupId']
            item.package_group = self.package_group_lookup[
                item.package_group_id]
            item.postage_service_id = request['PostalServiceId']
            item.postage_service = self.postal_service_lookup[
                item.postage_service_id]
            item.tax_rate = request['TaxRate']
            item.variation_group_name = request['VariationGroupName']
            item.weight = request['Weight']
            item.width = request['Width']

    def get_extended_properties(self):
        for item in self.items:
            request = self.api.get_inventory_item_extended_properties(
                item.stock_id)
            for prop in request:
                property_name = prop['ProperyName']  # sic
                if property_name not in self.extended_properties:
                    self.extended_properties.append(property_name)
            for prop in self.extended_properties:
                item.extended_properties[prop] = ''
            for prop in request:
                item.extended_properties[prop['ProperyName']] = prop[
                    'PropertyValue']

    def get_category_lookup(self):
        category_info = self.api.get_category_info()
        category_lookup = {}
        for category in category_info:
            category_lookup[category['id']] = category['name']
        return category_lookup

    def get_package_group_lookup(self):
        package_info = self.api.get_packaging_group_info()
        package_group_lookup = {}
        for group in package_info:
            package_group_lookup[group['id']] = group['name']
        return package_group_lookup

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
