"""Contains InventoryItem."""

import pylinnworks.api_requests as api_requests
from . extended_properties import ExtendedProperties
from . extended_property import ExtendedProperty
from . inventory_item_image import InventoryItemImage
from . inventory_item_images import InventoryItemImages


class InventoryItem:
    """Wrapper for linnworks inventory items."""

    def __init__(self, api_session, stock_id):
        self.api_session = api_session
        self.stock_id = stock_id

    def __repr__(self):
        return 'Inventory Item: {}'.format(self.stock_id)

    def __str__(self):
        return '{}: {}'.format(self.sku, self.title)

    def get_item_data(self):
        """Download current information for item."""
        get_item_request = api_requests.GetInventoryItemByID(
            self.api_session, self.stock_id)
        item_data = get_item_request.response_dict
        return item_data

    def get_prop(self, prop):
        """Get item property."""
        item_data = self.get_item_data()
        return item_data[prop]

    def set_prop(self, prop, value):
        """Set item property."""
        item_data = self.get_item_data()
        item_data[prop] = value
        self.update_item(item_data)

    def update_item(self, item_data):
        """Save item data for item."""
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

    @property
    def sku(self):
        """Get item SKU."""
        return self.get_prop('ItemNumber')

    @sku.setter
    def sku(self, sku):
        """Set item SKU."""
        return self.set_prop('ItemNumber', str(sku))

    @property
    def title(self):
        """Get item title."""
        return self.get_prop('ItemTitle')

    @title.setter
    def title(self, title):
        """Set item title."""
        return self.set_prop('ItemTitle', str(title))

    @property
    def barcode(self):
        """Get item barcode."""
        return self.get_prop('BarcodeNumber')

    @barcode.setter
    def barcode(self, barcode):
        """Set item barcode."""
        return self.set_prop('BarcodeNumber', str(barcode))

    @property
    def category_id(self):
        """Get item category ID."""
        return self.get_prop('CategoryId')

    @category_id.setter
    def category_id(self, cateogry_id):
        """Get item category ID."""
        return self.set_prop('CategoryId', str(cateogry_id))

    @property
    def package_group_id(self):
        """Get item package group ID."""
        return self.get_prop('PackageGroupId')

    @package_group_id.setter
    def package_group_id(self, package_group_id):
        """Set item package group ID."""
        return self.set_prop('PackageGroupId', str(package_group_id))

    @property
    def postage_service_id(self):
        """Get item postage service ID."""
        return self.get_prop('PostalServiceId')

    @postage_service_id.setter
    def postage_service_id(self, postage_service_id):
        """Set item postage service ID."""
        return self.set_prop('PostalServiceId', str(postage_service_id))

    @property
    def meta_data(self):
        """Get item meta data."""
        return self.get_prop('MetaData')

    @meta_data.setter
    def meta_data(self, meta_data):
        """Set item meta data."""
        return self.set_prop('MetaData', str(meta_data))

    @property
    def depth(self):
        """Get item depth."""
        return self.get_prop('Depth')

    @depth.setter
    def depth(self, depth):
        """Set item depth."""
        return self.set_prop('Depth', str(float(depth)))

    @property
    def width(self):
        """Get item width."""
        return self.get_prop('Width')

    @width.setter
    def width(self, width):
        """Set item width."""
        return self.set_prop('Width', str(float(width)))

    @property
    def height(self):
        """Get item height."""
        return self.get_prop('Height')

    @height.setter
    def height(self, height):
        """Set item height."""
        return self.set_prop('Height', str(float(height)))

    @property
    def purchase_price(self):
        """Get item purchase price."""
        return self.get_prop('PurchasePrice')

    @purchase_price.setter
    def purchase_price(self, purchase_price):
        """Set item purchase price."""
        return self.set_prop('PurchasePrice', str(float(purchase_price)))

    @property
    def retail_price(self):
        """Get item retail price."""
        return self.get_prop('RetailPrice')

    @retail_price.setter
    def retail_price(self, retail_price):
        """Set item retail price."""
        return self.set_prop('RetailPrice', str(float(retail_price)))

    @property
    def tax_rate(self):
        """Get item tax rate."""
        return self.get_prop('TaxRate')

    @tax_rate.setter
    def tax_rate(self, tax_rate):
        """Set item tax rate."""
        return self.set_prop('TaxRate', int(tax_rate))

    @property
    def quantity(self):
        """Get item quantity."""
        return self.get_prop('Quantity')

    @quantity.setter
    def quantity(self, quantity):
        """Set item quantity."""
        return self.set_prop('Quantity', int(quantity))

    def get_stock_levels(self):
        request = api_requests.GetStockLevel(self.api_session, self.stock_id)
        stock_levels = {}
        for location in request.response_dict:
            stock_levels[location['Location']['StockLocationId']] = {
                'available': location['Available'],
                'stock_level': location['StockLevel'],
                'in_orders': location['InOrders'],
                'due': location['Due'],
            }
        return stock_levels

    def get_available(
            self, location_id=None):
        if location_id is None:
            location_id = self.api_session.locations['Default'].guid
        stock_levels = self.get_stock_levels()
        return stock_levels[location_id]["Available"]

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
        prop = ExtendedProperty(self)
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
