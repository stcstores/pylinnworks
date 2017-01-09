from .. pylinnworks import PyLinnworks
from pylinnworks.api_requests import GetInventoryItemCount


class Inventory(PyLinnworks):
    def get_inventory_item(api_session, stock_id=None, sku=None):
        from pylinnworks.inventory import InventoryItem
        if stock_id is None and sku is None or stock_id is not None and \
                sku is not None:
            raise ValueError("Either stock_id or sku should be supplied")
        if sku is not None:
            stock_id = get_stock_id_by_SKU(api_session, sku)
        return InventoryItem(api_session, load_stock_id=stock_id)

    @classmethod
    def get_inventory_item_count(cls):
        request = GetInventoryItemCount(cls)
        return request.item_count

    def get_inventory(api_session, location='Default'):
        from pylinnworks.inventory.inventory import InventoryList
        from pylinnworks.inventory.extended_property import ExtendedProperty
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