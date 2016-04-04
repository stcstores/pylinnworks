from linnapi.api_requests.inventory.get_inventory_views \
    import GetInventoryViews
from linnapi.api_requests.inventory.get_inventory_items \
    import GetInventoryItems
from . inventory_item import InventoryItem as InventoryItem


class Inventory():

    def __init__(
            self, api_session, load=False, locations=None, item_list=None):
        self.api_session = api_session
        if locations is None:
            self.locations = [self.api_session.locations['Default']]
        else:
            locations = locations
        self.items = []
        self.skus = []
        self.stock_ids = []
        self.titles = []
        self.sku_lookup = {}
        self.stock_id_lookup = {}
        self.title_lookup = {}
        if items is not None:
            self.items = items
            self.update()
        elif load is True:
            self.load()

    def __getitem__(self, key):
        if key in self.stock_id_lookup:
            return self.items[stock_id_lookup[key]]
        elif key in self.sku_lookup:
            return self.items[self.sku_lookup[key]]
        elif key in self.title_lookup:
            return self.items[self.title_lookup[key]]
        else:
            return self.items[key]

    def __iter__(self):
        for item in self.items:
            yield item

    def __len__(self):
        return len(self.items)

    def append(self, item):
        self.items.append(item)
        self.update()

    def update(self):
        self.skus = []
        self.stock_ids = []
        self.titles = []
        self.sku_lookup = {}
        self.stock_id_lookup = {}
        self.title_lookup = {}
        for item in self.items:
            item_index = self.items.index(item)
            self.skus.append(item.sku)
            self.sku_lookup[item.sku] = item_index
            self.stock_ids.append(item.stock_id)
            self.stock_id_lookup[item.stock_id] = item_index
            self.titles.append(item.title)
            self.title_lookup[item.title] = item_index

    def load(self):
        locations = []
        for location in self.locations:
            locations.append(location.guid)
        view = GetInventoryViews(api_session)[0]
        self.request = GetInventoryItems(
            self.api_session, start=0, count=999999, view=view,
            locations=locations)
        for item_data in self.request.response_dict['Items']:
            self.add_item(item_data)
        self.update()

    def add_item(self, item_data):
        new_item = InventoryItem(self.api_session)
        new_item.load_from_request(item_data)

    def get_inventory_item_details(self):
        for item in self.items:
            request = self.api_session.get_inventory_item_by_id(item.stock_id)
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
            request = self.api_session.get_inventory_item_extended_properties(
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

    def to_table(self):
        from lstools import Table as Table
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
