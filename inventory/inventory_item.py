#!/usr/bin/env python3

"""This module contains the InventoryItem class to be used as a container for
Linnworks Inventory Items."""

import uuid
import json

import linnapi.api_requests as api_requests
from . extended_properties import ExtendedProperties
from . extended_property import ExtendedProperty
from . inventory_item_image import InventoryItemImage
from . inventory_item_images import InventoryItemImages


class InventoryItem:

    def __init__(self, api_session, stock_id=None, sku=None, title=None):
        self.api_session = api_session
        self.extended_properties = ExtendedProperties(self, False)
        if stock_id is not None:
            self.stock_id = stock_id
        if sku is not None:
            self.sku = sku
        if title is not None:
            self.title = title

    def __str__(self):
        return str(self.sku) + ': ' + str(self.title)

    def update_item(self, item_data):
        self.last_update_item_request = api_requests.UpdateInventoryItem(
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

    def load_extended_properties(self):
        request = api_requests.GetInventoryItemExtendedProperties(
            self.api_session, self.stock_id)
        response = request.response_dict
        for extended_property in response:
            new_property = ExtendedProperty(
                property_type=extended_property['PropertyType'],
                value=extended_property['PropertyValue'],
                name=extended_property['ProperyName'],
                property_id=extended_property['pkRowId'],
                item_stock_id=self.stock_id)
            self.extended_properties.append(new_property)

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

    def get_images_data(self):
        request = api_requests.GetInventoryItemImages(
            self.api_session, self.stock_id)
        return request.response_dict

    def get_images(self):
        images = []
        image_data = self.get_images_data()
        for image in image_data:
            images.append(InventoryItemImage(
                self.api_session, image['pkRowId'], self.stock_id,
                image['Source'], image['IsMain']))
        return InventoryItemImages(
            self.api_session, self, images=images)

    def add_image(self, filepath):
        """Add image to item.

        Arguments:
            filepath -- Path to image to be uploaded.
        """
        upload_request = api_requests.UploadFile(
            self.api_session, filepath, file_type='Image', expire_in=24)
        upload_response = upload_request.response_dict
        image_guid = upload_response[0]['FileId']
        return api_requests.UploadImagesToInventoryItem(
            self.api_session, self.stock_id, [image_guid])

    def get_item_data(self):
        get_item_request = api_requests.GetInventoryItemByID(
            self.api_session, self.stock_id)
        item_data = get_item_request.response_dict
        return item_data

    def get_prop(self, prop):
        item_data = self.get_item_data()
        return item_data[prop]

    def set_prop(self, prop, value):
        item_data = get_item_data()
        item_data[prop] = value
        self.update_item(item_data)

    def get_sku(self):
        return self.get_prop('ItemNumber')

    def get_title(self):
        return self.get_prop('ItemTitle')

    def get_barcode(self):
        return self.get_prop('BarcodeNumber')

    def get_category(self):
        return self.api_session.categories[
            self.get_prop('CategoryId')]

    def get_package_group(self):
        return self.api_session.package_groups[
            self.get_prop('PackageGroupId')]

    def get_postage_service(self):
        return self.api_session.postage_services[
            self.get_prop('PostalServiceId')]

    def get_category_id(self):
        return self.get_prop('CategoryId')

    def get_package_group_id(self):
        return self.get_prop('PackageGroupId')

    def get_postage_service_id(self):
        return self.get_prop('PostalServiceId')

    def get_meta_data(self):
        return self.get_prop('MetaData')

    def get_depth(self):
        return self.get_prop('Depth')

    def get_width(self):
        return self.get_prop('Width')

    def get_height(self):
        return self.get_prop('Height')

    def get_purchase_price(self):
        return self.get_prop('PurchasePrice')

    def get_retail_price(self):
        return self.get_prop('RetailPrice')

    def get_tax_rate(self):
        return self.get_prop('TaxRate')

    def get_quantity(self):
        return self.get_prop('Quantity')

    def set_sku(self, sku):
        return self.set_prop('ItemNumber', str(sku))

    def set_title(self, title):
        return self.set_prop('ItemTitle', str(title))

    def set_barcode(self, barcode):
        return self.set_prop('BarcodeNumber', str(barcode))

    def set_category_id(self, cateogry_id):
        return self.set_prop('CategoryId', str(cateogry_id))

    def set_package_group_id(self, package_group_id):
        return self.set_prop('PackageGroupId', str(package_group_id))

    def set_postage_service_id(self, postage_service_id):
        return self.set_prop('PostalServiceId', str(postage_service_id))

    def set_category(self, cateogry):
        return self.set_prop('CategoryId', str(cateogry_id.guid))

    def set_package_group(self, package_group):
        return self.set_prop('PackageGroupId', str(package_group_id.guid))

    def set_postage_service(self, postage_service):
        return self.set_prop('PostalServiceId', str(postage_service_id.guid))

    def set_meta_data(self, meta_data):
        return self.set_prop('MetaData', str(meta_data))

    def set_depth(self, depth):
        return self.set_prop('Depth', str(float(depth)))

    def set_width(self, width):
        return self.set_prop('Width', str(float(width)))

    def set_height(self, height):
        return self.set_prop('Height', str(float(height)))

    def set_purchase_price(self, purchase_price):
        return self.set_prop('PurchasePrice', str(float(purchase_price)))

    def set_retail_price(self, retail_price):
        return self.set_prop('RetailPrice', str(float(retail_price)))

    def set_tax_rate(self, tax_rate):
        return self.set_prop('TaxRate', int(tax_rate))

    def set_quantity(self, quantity):
        return self.set_prop('Quantity', int(quantity))
