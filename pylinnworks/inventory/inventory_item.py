"""Contains InventoryItem."""

from pylinnworks import api_requests
from . extended_properties import ExtendedProperties
from . extended_property import ExtendedProperty
from . inventory_item_images import InventoryItemImages
from .. settings import Settings


class InventoryItem:
    """Wrapper for linnworks inventory items.

    Attributes:
        api_session (:class: `PyLinnworks`): Login information for
            linnworks.net API.
        stock_id (int): Stock ID (GUID) for this item.
        images: Defaults to None. get_images method sets this to an instance
            of InventoryItemImages providing attributes of, and methods for
            working with this item's images.
        extended_properties: Defaults to None. get_extended_properties method
            sets this to instance of `ExtendedProperties` providing attributes
            of and method for working with this items's extended properties.
    """

    def __init__(self, api_session, stock_id):
        """Initialise InventoryItem.

        Arguments:
            api_session (:class: `PyLinnworks`): Login information for
                linnworks.net API.
            stock_id (int): Stock ID (GUID) for this item.
        """
        self.api_session = api_session
        self.stock_id = stock_id
        self.images = None
        self.extended_properties = None
        self.refresh()

    def __repr__(self):
        return 'Inventory Item: {}'.format(self.stock_id)

    def __str__(self):
        return '{}: {}'.format(self.sku, self.title)

    def refresh(self):
        """Populate this inventory item from linnworks.net servers."""
        item_data = self._get_item_data()
        self.variation_group_name = item_data['VariationGroupName']
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
        self.meta_data = item_data['MetaData']
        self.quantity = item_data['Quantity']
        self.in_order = item_data['InOrder']
        self.due = item_data['Due']
        self.minimum_level = item_data['MinimumLevel']
        self.available = item_data['Available']
        self.weight = item_data['Weight']
        self.width = item_data['Width']
        self.height = item_data['Height']
        self.depth = item_data['Depth']
        self.tax_rate = item_data['TaxRate']
        self.creation_date = item_data['CreationDate']
        self.is_composite_parent = item_data['IsCompositeParent']

    def save(self):
        """Save item data for item."""
        request = api_requests.UpdateInventoryItem(
            self.api_session, stock_id=self.stock_id, sku=self.sku,
            title=self.title, barcode=self.barcode,
            purchase_price=self.purchase_price, retail_price=self.retail_price,
            category_id=self.category.guid,
            package_group_id=self.package_group.guid,
            postal_service_id=self.postal_service.guid,
            category_name=self.category.name,
            package_group_name=self.package_group.name,
            postal_service_name=self.postal_service.name,
            meta_data=self.meta_data, quantity=self.quantity,
            in_order=self.in_order, due=self.due,
            minimum_level=self.minimum_level, available=self.available,
            weight=self.weight, width=self.width, height=self.height,
            depth=self.depth, variation_group_name=self.variation_group_name,
            tax_rate=self.tax_rate, creation_date=self.creation_date,
            is_composite_parent=self.is_composite_parent, dim='')
        return request

    def add_location(self, location=None):
        if location is None:
            location = Settings.get_location_by_name('Default')
        api_requests.AddItemLocations(data=[(self.stock_id, location)])

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

    def get_extended_properties(self):
        """Get extended properties for this inventory item.

        Sets attribue `extended_properties` to `ExtendedProperties` allowing
        interaction with this item's extended properties.

        Returns:
            :obj: `ExtendedProperties`
        """
        self.extended_properties = ExtendedProperties(self)

    def get_images(self):
        """Get images for this inventory item.

        Sets attribute images to InventoryItemImages containing data about
        this item's images.

        Returns :class: `InventoryItemImages`
        """
        self.images = InventoryItemImages(self.api_session, self.stock_id)
        return self.images

    def add_image(self, filepath):
        """Add image to item.

        Arguments:
            filepath -- Path to image to be uploaded.
        """
        upload_request = api_requests.UploadFile(
            self.api_session, filepath, file_type='Image', expire_in=24)
        upload_response = upload_request.response_dict
        image_guid = upload_response[0]['FileId']
        api_requests.UploadImagesToInventoryItem(
            self.api_session, self.stock_id, [image_guid])
        self.get_images()

    def _get_item_data(self):
        get_item_request = api_requests.GetInventoryItemByID(
            self.api_session, self.stock_id)
        item_data = get_item_request.response_dict
        return item_data
