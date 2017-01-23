from .. request import Request


class UpdateInventoryItem(Request):
    url_extension = '/api/Inventory/UpdateInventoryItem'

    def __init__(
            self, api_session, stock_id, sku='', title='', barcode='',
            purchase_price=0.0, retail_price=0.0, category_id=None,
            package_group_id=None, postal_service_id=None,
            postal_service_name=None, category_name=None,
            package_group_name=None, meta_data='', quantity=0, in_order=0,
            due=0, minimum_level=0, available=0, weight=0, width=0, depth=0,
            height=0, variation_group_name='', tax_rate=-1, creation_date=None,
            is_composite_parent=None, dim=0):
        self.stock_id = stock_id
        self.sku = sku
        self.title = title
        self.barcode = barcode
        self.purchase_price = purchase_price
        self.retail_price = retail_price
        self.category_id = category_id
        self.package_group_id = package_group_id
        self.postal_service_id = postal_service_id
        self.category_name = category_name
        self.package_group_name = package_group_name
        self.postal_service_name = postal_service_name
        self.meta_data = meta_data
        self.quantity = quantity
        self.in_order = in_order
        self.due = due
        self.minimum_level = minimum_level
        self.available = available
        self.weight = weight
        self.width = width
        self.depth = depth
        self.height = height
        self.variation_group_name = variation_group_name
        self.tax_rate = tax_rate
        self.creation_date = creation_date
        self.is_composite_parent = is_composite_parent
        self.dim = dim

    def get_data(self):
        self.data = {
            "StockItemId": str(self.stock_id),
            "ItemNumber": str(self.sku),
            "ItemTitle": str(self.title),
            "BarcodeNumber": str(self.barcode),
            "PurchasePrice": float(self.purchase_price),
            "RetailPrice": float(self.retail_price),
            "CategoryId": self.category_id,
            "PackageGroupId": self.package_group_id,
            "PostalServiceId": self.postal_service_id,
            "PostalServiceName": self.postal_service_name,
            "CategoryName": self.category_name,
            "PackageGroupName": self.package_group_name,
            "MetaData": str(self.meta_data),
            "Quantity": int(self.quantity),
            "InOrder": int(self.in_order),
            "Due": int(self.due),
            "MinimumLevel": int(self.minimum_level),
            "Available": int(self.available),
            "Weight": int(self.weight),
            "Width": self.width,
            "Depth": self.depth,
            "Height": self.hgight,
            "VariationGroupName": self.variation_group_name,
            "TaxRate": int(self.tax_rate),
            "CreationDate": self.creation_date,
            "IsCompositeParent": self.is_composite_parent,
            "Dim": self.dim,
        }
        return self.data
