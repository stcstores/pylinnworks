"""Requests creation of new inventory item. """

import json

from .. request import Request
from .. functions import is_guid
from .. info . get_categories import GetCategories
from .. info . get_package_groups import GetPackageGroups
from .. info . get_postage_services import GetPostageServices


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
                 height=None):
        self.sku = sku
        self.stock_id = stock_id
        self.title = title
        if barcode is not None:
            self.barcode = barcode
        if purchase_price is not None:
            self.purchase_price = float(purchase_price)
        if retail_price is not None:
            self.retail_price = float(retail_price)
        if quantity is not None:
            self.quantity = quantity
        if tax_rate is not None:
            self.tax_rate = tax_rate
        if variation_group_name is not None:
            self.variation_group_name = variation_group_name
        if meta_data is not None:
            self.meta_data = meta_data
        if category_id is not None:
            self.category_id = category_id
        elif self.category_id is None:
            self.category_id = GetCategories.default
        if package_group_id is not None:
            self.package_group_id = package_group_id
        elif self.package_group_id is None:
            self.package_group_id = GetPackageGroups.default
        if postage_service_id is not None:
            self.postage_service_id = postage_service_id
        elif self.postage_service_id is None:
            self.postage_service_id = GetPostageServices.default
        if weight is not None:
            self.weight = weight
        if width is not None:
            self.width = width
        if depth is not None:
            self.depth = depth
        if height is not None:
            self.height = height
        super().__init__(api_session)

    def test_request(self):
        assert isinstance(self.sku, str), "SKU must be string."
        assert len(self.sku) > 0, "SKU must not be empty string."
        assert is_guid(self.stock_id), "Stock ID must be valid GUID"
        assert isinstance(self.title, str), "Title must be string."
        assert len(self.title) > 0, "Title must not be empty string."
        assert isinstance(self.barcode, str), "Barcode must be string."
        assert isinstance(self.purchase_price, float), \
            "Purchase Price must be float."
        assert isinstance(self.retail_price, float), \
            "Retail Price must be float."
        assert isinstance(self.quantity, int), "Quantity must be int."
        assert isinstance(self.tax_rate, int), "Tax Rate must be int."
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
