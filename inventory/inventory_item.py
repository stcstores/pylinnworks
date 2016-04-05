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


class InventoryItem:
    stock_id = None
    sku = ''
    title = ''
    purchase_price = 0
    retail_price = 0
    barcode = ''
    category = ''
    depth = ''
    height = ''
    package_group = ''
    postage_service = ''
    tax_rate = 0
    variation_group_name = ''
    weight = 0
    width = 0
    available = 0
    meta_data = ''
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
        from linnapi.api_requests.inventory.get_inventory_item_by_id \
            import GetInventoryItemByID
        get_item_request = GetInventoryItemByID(
            self.api_session, self.stock_id)
        item_data = get_item_request.response_dict
        from pprint import pprint
        pprint(item_data)
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

        from linnapi.api_requests.inventory.inventory_view import InventoryView
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

    def create_sku(self):
        """Returns new *SKU*."""
        self.sku = GetNewSKU(self.api_session).sku

    def get_create_inventoryItem_dict(self):
        """Return ``dict`` for use with ``AddInventoryItem`` API request."""
        inventoryItem = {}
        inventoryItem['ItemNumber'] = str(self.sku)
        inventoryItem['ItemTitle'] = str(self.title)
        inventoryItem['BarcodeNumber'] = str(self.barcode)
        inventoryItem['PurchasePrice'] = str(self.purchase_price)
        inventoryItem['RetailPrice'] = str(self.retail_price)
        inventoryItem['Quantity'] = str(self.quantity)
        inventoryItem['TaxRate'] = str(self.tax_rate)
        inventoryItem['StockItemId'] = str(self.stock_id)
        return inventoryItem

    def get_inventoryItem_dict(self):
        """Return ``dict`` for use with ``UpdateInventoryItem`` API request."""
        inventoryItem = {}
        inventoryItem['ItemNumber'] = str(self.sku)
        inventoryItem['ItemTitle'] = str(self.title)
        inventoryItem['BarcodeNumber'] = str(self.barcode)
        inventoryItem['PurchasePrice'] = str(self.purchase_price)
        inventoryItem['RetailPrice'] = str(self.retail_price)
        inventoryItem['Quantity'] = str(self.quantity)
        inventoryItem['TaxRate'] = str(self.tax_rate)
        inventoryItem['StockItemId'] = str(self.stock_id)
        inventoryItem['VariationGroupName'] = str(self.variation_group_name)
        inventoryItem['MetaData'] = str(self.meta_data)
        inventoryItem['CategoryId'] = str(self.category_id)
        inventoryItem['PackageGroupId'] = str(self.package_group_id)
        inventoryItem['PostalServiceId'] = str(self.postage_service_id)
        inventoryItem['Weight'] = str(self.weight)
        inventoryItem['Width'] = str(self.width)
        inventoryItem['Depth'] = str(self.depth)
        inventoryItem['Height'] = str(self.height)
        return inventoryItem

    def create_item(self):
        """Make request to create new *inventory item* on Linnworks server."""
        for prop in (self.stock_id, self.sku, self.title):
            assert(prop is not None)
        inventoryItem = self.get_create_inventoryItem_dict()
        request_url = self.api_session.server + '/api/Inventory/AddInventoryItem'
        data = {'inventoryItem': json.dumps(inventoryItem)}
        return self.api_session.request(request_url, data)

    def update_item(self):
        """Make request to create update existing *inventory item* on Linnworks
        server.
        """
        for prop in (self.stock_id, self.sku, self.title):
            assert(prop is not None)
        inventoryItem = self.get_inventoryItem_dict()
        request_url = self.api_session.server + '/api/Inventory/UpdateInventoryItem'
        data = {'inventoryItem': json.dumps(inventoryItem)}
        return self.api_session.request(request_url, data)

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
