"""Requests creation of new inventory item. """

import json

from linnapi.api_requests.request import Request
from linnapi.functions import is_guid


class AddInventoryItem(Request):
    url_extension = '/api/Inventory/AddInventoryItem'

    sku = ''
    stock_id = ''
    title = ''
    barcode = ''
    purchase_price = 0.0
    retail_price = 0.0
    quantity = 0
    tax_rate = 0
    variation_group_name = ''
    meta_data = ''
    category_id = None
    package_group_id = None
    postage_service_id = None
    weight = 0
    width = 0
    depth = 0
    height = 0

    def __init__(self,
                 api_session, stock_id, sku, title, barcode=None,
                 purchase_price=None, retail_price=None, quantity=None,
                 tax_rate=None, variation_group_name=None, meta_data=None,
                 category_id=None, package_group_id=None,
                 postage_service_id=None, weight=None, width=None, depth=None,
                 height=None, test=True):
        self.sku = str(sku)
        self.stock_id = str(stock_id)
        self.title = str(title)
        self.barcode = str(barcode)
        self.purchase_price = float(purchase_price)
        self.retail_price = float(retail_price)
        self.quantity = int(quantity)
        self.tax_rate = float(tax_rate)
        self.variation_group_name = str(variation_group_name)
        self.meta_data = str(meta_data)
        self.category_id = str(category_id)
        self.package_group_id = str(package_group_id)
        self.postage_service_id = str(postage_service_id)
        self.weight = float(weight)
        self.width = float(width)
        self.depth = float(depth)
        self.height = float(height)
        super().__init__(api_session, test)

    def test_request(self):
        assert isinstance(self.sku, str), "SKU must be string."
        assert len(self.sku) > 0, "SKU must not be empty string."
        assert is_guid(self.stock_id), "Stock ID must be valid GUID"
        return super().test_request()

    def get_data(self):
        inventory_item = {
            'ItemNumber': str(self.sku),
            'ItemTitle': str(self.title),
            'BarcodeNumber': str(self.barcode),
            'PurchasePrice': str(self.purchase_price),
            'RetailPrice': str(self.retail_price),
            'Quantity': str(self.quantity),
            'TaxRate': str(self.tax_rate),
            'StockItemId': str(self.stock_id),
            'VariationGroupName': str(self.variation_group_name),
            'MetaData': str(self.meta_data),
            'CategoryId': str(self.category_id),
            'PackageGroupId': str(self.package_group_id),
            'PostalServiceId': str(self.postage_service_id),
            'Weight': str(self.weight),
            'Width': str(self.width),
            'Depth': str(self.depth),
            'Height': str(self.height),
        }
        data = {'inventoryItem': json.dumps(inventory_item)}
        return data
