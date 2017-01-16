"""
Inventory Class used for managing Linnworks stock inventory.

Provides methods for finding and manipulating inventory items.
"""

from .. pylinnworks import PyLinnworks
from pylinnworks.api_requests import SKUExists
from . inventory_item import InventoryItem
from . extended_property import ExtendedProperty


class Inventory(PyLinnworks):
    """Provide methods for finding and interacting with inventory items."""

    @classmethod
    def search_inventory(cls, view=None, filters=[], locations=None):
        """Create API request to search for inventory items."""
        if view is None:
            view = InventoryView()
        view.filters = filters
        if locations is None:
            locations = [location.guid for location in Settings().locations]
        view.locations = locations
        response = GetInventoryItems(cls, view=view, locations=locations)

    @classmethod
    def get_inventory_item(cls, stock_id=None, sku=None):
        """Get inventory item by stock ID (GUID) or SKU."""
        if stock_id is None and sku is None or stock_id is not None and \
                sku is not None:
            raise ValueError("Either stock_id or sku should be supplied")
        if sku is not None:
            stock_id = cls.get_stock_id_by_SKU(cls, sku)
        return InventoryItem(cls, load_stock_id=stock_id)

    @classmethod
    def get_stock_id_by_SKU(cls, sku):
        """Return stock ID (GUID) of item with SKU sku."""
        locations = [location.guid for location in Settings().locations]
        view = InventoryView()
        view.filters.append(InventoryViewFilter(
            field='String',
            value=sku,
            condition='Equals',
            filter_name='SKU',
            filter_name_exact=''
        ))
        response = GetInventoryItems(cls, view=view, locations=locations)
        return response.response_dict['Items'][0]['Id']

    @classmethod
    def get_inventory_item_count(cls):
        """Get number of items in inventory."""
        request = GetInventoryItemCount(cls)
        return request.item_count

    @classmethod
    def SKU_exists(cls, sku):
        """Check if sku has been used as a product SKU."""
        request = SKUExists(cls, sku)
        return request.response_dict

    @classmethod
    def get_inventory(api_session, location='Default'):
        inventory = Inventory(api_session, load=True)
        inventory_export = get_export(
            api_session, script_id=8, parameters=[
                {"Type": "Select", "Name": "locationName", "Value": location}])
        extended_properties_export = get_export(
            api_session, script_id=57, parameters=[
                {"Type": "String", "Name": "SKU", "Value": ""},
                {"Type": "String", "Name": "Property", "Value": ""}])
        inventory_lookup = {}
        for row in inventory_export:
            inventory_lookup[row['SKU']] = row
        extended_properties_lookup = {}
        for row in extended_properties_export:
            if row['SKU'] not in extended_properties_lookup:
                extended_properties_lookup[row['SKU']] = []
            extended_properties_lookup[row['SKU']].append(row)
        for item in inventory:
            i_row = inventory_lookup[item.sku]
            item.title = i_row['ItemTitle']
            item.meta_data = i_row['ItemDescription']
            item.retail_price = float(i_row['RetailPrice'])
            item.purchase_price = float(i_row['PurchasePrice'])
            item.weight = float(i_row['Weight'])
            item.barcode = i_row['BarcodeNumber']
            item.height = float(i_row['DimHeight'])
            item.width = float(i_row['DimWidth'])
            item.depth = float(i_row['DimDepth'])
            item.tax_rate = float(i_row['TaxRate'])
            item.category = api_session.categories[i_row['CategoryName']]
            try:
                item.postage_service = api_session.postage_services[
                    i_row['DefaultPostalService']]
            except:
                pass
            item.package_group = api_session.package_groups[
                i_row['DefaultPackagingGroup']]
            item.available = i_row['Available']
            item.bin_rack = i_row['BinRack']
            if item.sku in extended_properties_lookup:
                for e_row in extended_properties_lookup[item.sku]:
                    new_extended_property = ExtendedProperty(
                        property_type=e_row['PropertyType'],
                        value=e_row['PropertyValue'], name=e_row['Property'],
                        item_stock_id=item.stock_id)
                    item.extended_properties.append(new_extended_property)
