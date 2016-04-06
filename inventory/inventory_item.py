#!/usr/bin/env python3

"""This module contains the ``InventoryItem`` class to be used as a container
for Linnworks Inventory Items."""

import uuid
import json

from linnapi.api_requests.inventory.get_inventory_column_types \
    import GetInventoryColumnTypes
from linnapi.api_requests.inventory.inventory_view_filter\
    import InventoryViewFilter
from linnapi.api_requests.inventory.get_inventory_items \
    import GetInventoryItems
from linnapi.api_requests.inventory.update_inventory_item \
    import UpdateInventoryItem
from linnapi.api_requests.inventory.get_inventory_item_by_id \
    import GetInventoryItemByID
from linnapi.api_requests.inventory.inventory_view import InventoryView


class InventoryItem:
    stock_id = None
    sku = None
    title = None
    purchase_price = None
    retail_price = None
    barcode = None
    category = None
    depth = None
    height = None
    package_group = None
    postage_service = None
    tax_rate = None
    variation_group_name = None
    weight = None
    width = None
    available = None
    meta_data = None
    bin_rack = None
    extended_properties = None

    def __init__(self, api_session, stock_id=None, sku=None, title=None,
                 purchase_price=None, retail_price=None, barcode=None,
                 category=None, depth=None, height=None, package_group=None,
                 postage_service=None, tax_rate=None,
                 variation_group_name=None, weight=None, width=None,
                 available=None, meta_data=None, bin_rack=None,
                 extended_properties=None, load_stock_id=None):
        self.api_session = api_session
        if load_stock_id is not None:
            self.load_from_stock_id(load_stock_id)
        if stock_id is not None:
            self.stock_id = stock_id
        if sku is not None:
            self.sku = sku
        if title is not None:
            self.title = title
        if purchase_price is not None:
            self.purchase_price = purchase_price
        if retail_price is not None:
            self.retail_price = retail_price
        if barcode is not None:
            self.barcode = barcode
        if category is not None:
            self.category = category
        if depth is not None:
            self.depth = depth
        if height is not None:
            self.height = height
        if package_group is not None:
            self.package_group = package_group
        if postage_service is not None:
            self.postage_service = postage_service
        if tax_rate is not None:
            self.tax_rate = tax_rate
        if variation_group_name is not None:
            self.variation_group = variation_group
        if weight is not None:
            self.weight = weight
        if width is not None:
            self.width = width
        if available is not None:
            self.available = available
        if meta_data is not None:
            self.meta_data = meta_data
        if extended_properties is not None:
            self.extended_properties = extended_properties

    def __str__(self):
        return str(self.sku) + ': ' + str(self.title)

    def load_from_stock_id(self, stock_id):
        self.stock_id = stock_id
        self.load_all()

    def load_from_request(self, item_data):
        self.stock_id = item_data['Id']
        self.sku = item_data['SKU']
        self.barcode = item_data['Barcode']
        self.quantity = item_data['StockLevel']
        self.title = item_data['Title']
        self.category = self.api_session.categories[item_data['Category']]
        self.purchase_price = item_data['PurchasePrice']
        self.retail_price = item_data['RetailPrice']
        self.available = item_data['Available']
        self.bin_rack = item_data['BinRack']

    def load_all(self):
        get_item_request = GetInventoryItemByID(
            self.api_session, self.stock_id)
        item_data = get_item_request.response_dict
        if item_data['PostalServiceId'] \
                != '16a52bf9-47e5-44a2-aa38-15d6742dd84a':
            self.postage_service = self.api_session.postage_services[
                item_data['PostalServiceId']]
        else:
            self.postage_service = self.api_session.postage_services['Default']
        self.sku = item_data['ItemNumber']
        self.barcode = item_data['BarcodeNumber']
        self.depth = item_data['Depth']
        self.height = item_data['Height']
        self.meta_data = item_data['MetaData']
        self.package_group = self.api_session.package_groups[
            item_data['PackageGroupId']]
        self.purchase_price = item_data['PurchasePrice']
        self.tax_rate = item_data['TaxRate']
        self.variation_group_name = item_data['VariationGroupName']
        self.weight = item_data['Weight']
        self.width = item_data['Width']

        locations = self.api_session.locations.ids
        view = InventoryView()
        columns_request = GetInventoryColumnTypes(self.api_session)
        view.columns = columns_request.columns
        view_filter = InventoryViewFilter(
            field='SKU', value=self.sku, condition='equals')
        view.filters = [view_filter]
        inventory_request = GetInventoryItems(
            self.api_session, start=0, count=1, view=view,
            locations=locations)
        self.load_from_request(inventory_request.response_dict['Items'][0])
#       self.load_extended_properties()

    def set_empty_fields_to_default(self):
        from linnapi.functions import get_new_SKU
        if self.title is None or self.title == '':
            raise ValueError("Cannot create item without title")
        if self.stock_id is None:
            self.stock_id = str(uuid.uuid4())
        else:
            stock_id = self.stock_id
        if self.sku is None:
            self.sku = get_new_SKU(self.api_session)
        if self.barcode is None:
            self.barcode = ''
        if self.purchase_price is None:
            self.purchase_price = 0
        if self.retail_price is None:
            self.purchase_price = 0
        if self.available is None:
            self.available = 0
        if self.tax_rate is None:
            self.tax_rate = 0
        if self.variation_group_name is None:
            self.variation_group_name = ''
        if self.meta_data is None:
            self.meta_data = ''
        if self.category is None:
            self.category = self.api_session.categories['Default']
        if self.package_group is None:
            self.package_group = self.api_session.package_groups['Default']
        if self.postage_service is None:
            self.postage_service = self.api_session.postage_services['Default']
        if self.weight is None:
            self.weight = 0
        if self.width is None:
            self.width = 0
        if self.depth is None:
            self.depth = 0
        if self.height is None:
            self.height = 0

    def get_inventory_item_dict(self):
        self.set_empty_fields_to_default()
        item_data = {}
        item_data['ItemNumber'] = str(self.sku)
        item_data['ItemTitle'] = str(self.title)
        item_data['BarcodeNumber'] = str(self.barcode)
        item_data['PurchasePrice'] = str(float(self.purchase_price))
        item_data['RetailPrice'] = str(float(self.retail_price))
        item_data['Quantity'] = int(self.available)
        item_data['TaxRate'] = int(self.tax_rate)
        item_data['StockItemId'] = str(self.stock_id)
        item_data['VariationGroupName'] = str(self.variation_group_name)
        item_data['MetaData'] = str(self.meta_data)
        item_data['CategoryId'] = str(self.category.guid)
        item_data['PackageGroupId'] = str(self.package_group.guid)
        item_data['PostalServiceId'] = str(self.postage_service.guid)
        item_data['Weight'] = str(float(self.weight))
        item_data['Width'] = str(float(self.width))
        item_data['Depth'] = str(float(self.depth))
        item_data['Height'] = str(float(self.height))
        return item_data

    def create_item(self):
        from linnapi.api_requests.inventory.add_inventory_item \
            import AddInventoryItem
        item_data = self.get_inventory_item_dict()
        self.add_item_request = AddInventoryItem(
            self.api_session, item_data['StockItemId'],
            item_data['ItemNumber'], item_data['ItemTitle'],
            barcode=item_data['BarcodeNumber'],
            purchase_price=item_data['PurchasePrice'],
            retail_price=item_data['RetailPrice'],
            quantity=item_data['Quantity'], tax_rate=item_data['TaxRate'],
            variation_group_name=item_data['VariationGroupName'],
            meta_data=item_data['MetaData'],
            category_id=item_data['CategoryId'],
            package_group_id=item_data['PackageGroupId'],
            postage_service_id=item_data['PostalServiceId'],
            weight=item_data['Weight'], width=item_data['Width'],
            depth=item_data['Depth'], height=item_data['Height'])
        self.update_item()

    def update_item(self):
        self.set_empty_fields_to_default()
        item_data = self.get_inventory_item_dict()
        self.add_item_request = UpdateInventoryItem(
            self.api_session, item_data['StockItemId'],
            item_data['ItemNumber'], item_data['ItemTitle'],
            barcode=item_data['BarcodeNumber'],
            purchase_price=item_data['PurchasePrice'],
            retail_price=item_data['RetailPrice'],
            quantity=item_data['Quantity'], tax_rate=item_data['TaxRate'],
            variation_group_name=item_data['VariationGroupName'],
            meta_data=item_data['MetaData'],
            category_id=item_data['CategoryId'],
            package_group_id=item_data['PackageGroupId'],
            postage_service_id=item_data['PostalServiceId'],
            weight=item_data['Weight'], width=item_data['Width'],
            depth=item_data['Depth'], height=item_data['Height'])

    def update_all(self):
        """Update *inventory item* and it's *extended properties* on Linnworks
        server.
        """
        self.update_item()
        self.extended_properties.update()

    def load_extended_properties(self):
        """Get *extended properties* for item from Linnworks server."""
        self.extended_properties.load()

    def get_extended_properties_dict(self):
        """Return ``dict`` containing *extended_properties* names and
        values.
        """
        properties = {}
        for prop in self.extended_properties:
            if prop.delete is False:
                properties[prop.name] = prop.value
        return properties

    def get_extended_properties_list(self):
        """Return ``list`` containing ``dict``s of *extended properties*
        details.
        """
        properties = []
        for prop in self.extended_properties:
            if prop.delete is False:
                new_prop = {
                    'name': prop.name,
                    'value': prop.value,
                    'type': prop.type,
                    'guid': prop.guid
                }
                properties.append(new_prop)
        return properties

    def create_extended_property(self, name='', value='',
                                 property_type='Attribute'):
        """Add extended property to item.

        Arguments:
            name -- Name of new extended property.
            value -- Value of new extended prperty.

        Keyword Arguments:
            property_type -- Type of new extended property
                Defaults to 'Attribute'.
        """
        prop = _ExtendedProperty(self)
        prop.name = name
        prop.value = value
        prop.type = property_type
        self.extended_properties.append(prop)

    def add_image(self, filepath):
        """Add image to item.

        Arguments:
            filepath -- Path to image to be uploaded.
        """
        upload_response = self.api_session.upload_image(filepath)
        image_guid = upload_response[0]['FileId']
        add_url = self.api_session.server + (
            '/api/Inventory/UploadImagesToInventoryItem')
        add_data = {
            'inventoryItemId': self.stock_id,
            'imageIds': json.dumps([image_guid])}
        add_response = self.api_session.request(add_url, data=add_data)
        return add_response
