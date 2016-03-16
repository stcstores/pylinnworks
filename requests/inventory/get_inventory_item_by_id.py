"""Returns inventory item data for the item with the specifed stock id.

Arguments:
    stock_id -- GUID of inventory item.
"""

from .. request import Request
from linnapi.basic_item import BasicItem


class GetInventoryItemByID(Request):
    url_extension = '/api/Inventory/GetInventoryItemById'

    def __init__(self, api, stock_id):
        self.stock_id = stock_id
        super().__init__(api)

    def get_data(self):
        data = {'id': self.stock_id}
        self.data = data
        return data

    def to_basic_item(self):
        item_data = self.response_dict
        item = BasicItem()
        item.guid = self.stock_id
        item.sku = item_data['ItemNumber']
        item.title = item_data['ItemTitle']
        item.purchase_price = item_data['PurchasePrice']
        item.retail_price = item_data['RetailPrice']
        item.barcode = item_data['BarcodeNumber']
        item.category_id = item_data['CategoryId']
        item.depth = item_data['Depth']
        item.height = item_data['Height']
        item.package_group_id = item_data['PackageGroupId']
        item.postage_service_id = item_data['PostalServiceId']
        item.tax_rate = item_data['TaxRate']
        item.variation_group_name = item_data['VariationGroupName']
        item.weight = item_data['Weight']
        item.width = item_data['Width']
        item.meta_data = item_data['MetaData']
        item.quantity = self.api.get_stock_level_by_id(self.stock_id)
        for category in self.api.get_category_info():
            if category['id'] == item.category_id:
                item.category = category['name']
        for package_group in self.api.get_packaging_group_info():
            if package_group['id'] == item.package_group_id:
                item.package_group = package_group['name']
        for postage_service in self.api.get_shipping_method_info():
            if postage_service['id'] == item.postage_service:
                item.postage_service = postage_service['name']
        return item
