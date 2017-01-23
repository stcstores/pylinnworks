"""Contains InventoryItem."""

import pylinnworks.api_requests as api_requests
from . extended_properties import ExtendedProperties
from . extended_property import ExtendedProperty
from . inventory_item_image import InventoryItemImage
from . inventory_item_images import InventoryItemImages
from .. settings import Settings


class InventoryItem:
    """Wrapper for linnworks inventory items."""

    def __init__(self, api_session, stock_id):
        self.api_session = api_session
        self.stock_id = stock_id
        self.refresh()

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

    def refresh(self):
        """Populate this inventory item from linnworks.net servers."""
        item_data = self.get_item_data()
        self.sku = item_data['ItemNumber']
        self.title = item_data['ItemTitle']
        self.barcode = item_data['BarcodeNumber']
        self.purchase_price = item_data['PurchasePrice']
        self.retail_price = item_data['RetailPrice']
        self.category = Settings.get_category_by_ID(item_data['CategoryId'])
        self.package_group = Settings.get_package_group_by_ID(
            item_data['PackageGroupId'])
        self.postal_service = Settings.get_postage_service_by_ID(
            item_data['PostalServiceId'])
        self.quantity = item_data['Quantity']
        self.in_order = item_data['InOrder']
        self.due = item_data['Due']
        self.minimum_level = item_data['MinimumLevel']
        self.available = item_data['Available']
        self.weight = item_data['Weight']
        self.width = item_data['Width']
        self.height = item_data['Height']
        self.depth = item_data['Depth']
        self.creation_date = item_data['CreationDate']
        self.is_composite_parent = item_data['IsCompositeParent']

    def update_item(self, item_data):
        """Save item data for item."""
        api_requests.UpdateInventoryItem(
            self.api_session, stock_id=self.stock_id, sku=self.sku,
            title=self.title, barcode=self.barcode,
            purchase_price=self.purchase_price, retail_price=self.retail_price,
            category_id=self.category.guid,
            PackageGroupId=self.package_group.guid,
            package_group_id=self.package_group.guid,
            postal_service_id=self.postal_service.id,
            category_name=self.category.name,
            package_group_name=self.package_group.name,
            postal_service_name=self.postal_service.name,
            meta_data=self.meta_data, quantity=self.quantity,
            in_order=self.in_order, due=self.due,
            minimum_level=self.minimum_level, available=self.available,
            weight=self.weight, width=self.width, height=self.height,
            depth=self.depth, variation_group_name=self.variation_group_name,
            tax_rate=self.tax_rate, creation_date=self.creation_date,
            is_composite_parent=self.is_composite_parent, dim=self.dim)

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
