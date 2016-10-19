import pylinnworks.api_requests as api_requests
from . single_inventory_item import SingleInventoryItem
from . variation_group import VariationGroup
from . variation_inventory_item import VariationInventoryItem
from . inventory_items import InventoryItems
from pylinnworks.functions import get_inventory_item_count


class Inventory():

    def __init__(self, api_session, locations=None):
        self.api_session = api_session
        if locations is None:
            self.locations = [self.api_session.locations['Default']]
        else:
            locations = locations
        self.clear()

    def __getitem__(self, key):
        if key in self.stock_id_lookup:
            return self.items[self.stock_id_lookup[key]]
        elif key in self.sku_lookup:
            return self.items[self.sku_lookup[key]]
        elif key in self.title_lookup:
            return self.items[self.title_lookup[key]]
        else:
            return self.single_items[key]

    def __iter__(self):
        for item in self.single_items:
            yield item

    def __len__(self):
        return len(self.single_items)

    def clear(self):
        self.single_items = InventoryItems()
        self.variation_groups = InventoryItems()
        self.variation_children = InventoryItems()
        self.skus = []
        self.stock_ids = []
        self.titles = []

        self.sku_lookup = {}
        self.stock_id_lookup = {}
        self.title_lookup = {}

    def search_inventory(self, filters):
        view = api_requests.InventoryView()
        view.columns = []
        view.filters = filters
        locations = []
        for location in self.locations:
            locations.append(location.guid)
        request = api_requests.GetInventoryItems(
            self.api_session, start=0, count=100, view=view,
            locations=locations)
        self.load_from_get_inventory_items_request(request)

    def search_single_item_title(self, sku, condition='contains'):
        self.clear()
        filters = [api_requests.InventoryViewFilter(
            field='Title', value=sku, condition=condition)]
        self.search_inventory(filters)

    def search_single_item_sku(self, sku, condition='equals'):
        self.clear()
        filters = [api_requests.InventoryViewFilter(
            field='SKU', value=sku, condition=condition)]
        self.search_inventory(filters)

    def search_variation_title(self, title):
        request = api_requests.SearchVariationGroups(
            self.api_session, search_type='VariationName', search_text=title,
            page_number=1, count=100)
        self.load_from_search_variation_groups_request(request)

    def search_variation_sku(self, sku):
        request = api_requests.SearchVariationGroups(
            self.api_session, search_type='ParentSKU', search_text=sku,
            page_number=1, count=100)
        self.load_from_search_variation_groups_request(request)

    def search_title(self, title):
        self.clear()
        self.search_single_item_title(title)
        self.search_variation_title(title)

    def search_sku(self, sku):
        self.clear()
        self.search_single_item_sku(sku)
        self.search_variation_sku(sku)

    def load_from_get_inventory_items_request(self, request):
        for item_data in request.response_dict['Items']:
            self.add_single_item(item_data)

    def load_from_search_variation_groups_request(self, request):
        for item_data in request.response_dict['Data']:
            self.add_variation_group(item_data)

    def add_single_item(self, item_data):
        stock_id = item_data['Id']
        sku = item_data['SKU']
        title = item_data['Title']
        new_item = SingleInventoryItem(
            self.api_session, stock_id=stock_id,
            sku=sku, title=title)
        self.single_items.append(new_item)
        self.stock_ids.append(new_item.stock_id)
        self.skus.append(new_item.sku)
        self.titles.append(new_item.title)

    def add_variation_group(self, item_data):
        new_group = VariationGroup(
            self.api_session,
            item_data['pkVariationItemId'],
            item_data['VariationSKU'],
            item_data['VariationGroupName'])
        children_data = new_group.get_children()
        for child in children_data:
            new_group.children.append(self.single_items[child['ItemNumber']])
        self.variation_groups.append(new_group)
        self.stock_ids.append(new_group.stock_id)
        self.skus.append(new_group.sku)
        self.titles.append(new_group.title)
        self.variation_children.extend(new_group.children)
        for child in new_group.children:
            self.stock_ids.append(child.stock_id)
            self.skus.append(child.sku)
            self.titles.append(child.title)

    def append(self, item):
        self.items.append(item)
        self.update()

    def update(self):
        for item in self.single_items:
            item_index = self.single_items.index(item)
            self.skus.append(item.sku)
            self.sku_lookup[item.sku] = item_index
            self.stock_ids.append(item.stock_id)
            self.stock_id_lookup[item.stock_id] = item_index
            self.titles.append(item.title)
            self.title_lookup[item.title] = item_index

    def load(self, verbose=False):
        self.clear()
        locations = []
        for location in self.locations:
            locations.append(location.guid)
        view = api_requests.InventoryView()
        columns_request = api_requests.GetInventoryColumnTypes(
            self.api_session)
        view.columns = columns_request.columns
        total_items = get_inventory_item_count(self.api_session)
        start = 1
        item_count = 0
        count = 100
        while item_count < total_items:
            request = api_requests.GetInventoryItems(
                self.api_session, start=start, count=count, view=view,
                locations=locations)
            for item_data in request.response_dict['Items']:
                self.add_single_item(item_data)
                item_count += 1
            if verbose is True:
                print(
                    "start:{} count:{} response:{} stored:{} total:{}".format(
                        start, count, len(request.response_dict['Items']),
                        len(self.single_items), total_items))
            start += count
            if item_count + count >= total_items:
                count = total_items - item_count
        self.update()

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

    def quantify(self):
        return {
            'Single Items': len(self.single_items),
            'Variation Groups': len(self.variation_groups),
            'Variation Children': len(self.variation_children)
        }
