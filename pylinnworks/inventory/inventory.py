"""
Inventory Class used for managing Linnworks stock inventory.

Provides methods for finding and manipulating inventory items.
"""

from .. pylinnworks import PyLinnworks
from pylinnworks.api_requests import SKUExists
from . inventory_search import InventorySearch
from . inventory_view_filter import InventoryViewFilter


class Inventory(PyLinnworks):
    """Provide methods for finding and interacting with inventory items."""

    @classmethod
    def search_inventory(cls, filters=[], locations=None, columns=None):
        """Create API request to search for inventory items."""
        return InventorySearch(
            cls, filters=filters, locations=locations, columns=columns)

    @classmethod
    def get_inventory_item(cls, stock_id=None, sku=None):
        """Get inventory item by stock ID (GUID) or SKU."""
        if stock_id is None and sku is None or stock_id is not None and \
                sku is not None:
            raise ValueError("Either stock_id or sku should be supplied")
        if sku is not None:
            return cls.get_item_by_SKU(sku)
        else:
            return cls.get_item_by_stock_ID(stock_id)

    @classmethod
    def get_stock_id_by_SKU(cls, sku):
        """Return stock ID (GUID) of item with SKU sku."""
        item = cls.get_item_by_SKU(sku)
        return item.stock_id

    @classmethod
    def get_item_by_SKU(cls, sku, locations=None):
        """Return Inventory Item with SKU sku."""
        filters = [InventoryViewFilter(
            field='SKU', value=sku)]
        item = InventorySearch(
            cls, filters=filters, locations=locations).get_item()
        return item

    @classmethod
    def search_by_SKU(cls, sku, locations=None):
        """Search inventory by SKU.

        Returns InventoryList.
        """
        filters = [InventoryViewFilter(
            filter_name='SKU', field='String', value=sku,
            condition='Contains')]
        inventory_list = InventorySearch(
            cls, filters=filters, locations=locations).get_items()
        return inventory_list

    @classmethod
    def get_item_by_stock_ID(cls, stock_id, locations=None):
        """Return Inventory Item with stock ID stock_id."""
        filters = [InventoryViewFilter(
            field='StockId', value=stock_id)]
        item = InventorySearch(
            cls, filters=filters, locations=locations).get_item()
        return item

    @classmethod
    def get_inventory_item_count(
            cls, view=None, locations=None, columns=None, filters=None):
        """Get number of items in inventory."""
        search = InventorySearch(
            cls, view=view, locations=locations, columns=columns,
            filters=filters)
        return search.count_items()

    @classmethod
    def SKU_exists(cls, sku):
        """Check if sku has been used as a product SKU."""
        request = SKUExists(cls, sku)
        return request.response_dict

    @classmethod
    def get_inventory(cls, locations=None):
        """Get all inventory."""
        return InventorySearch(cls, locations=locations)
