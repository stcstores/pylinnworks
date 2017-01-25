"""
Inventory Class used for managing Linnworks stock inventory.

Provides methods for finding and manipulating inventory items.
"""

import uuid

from .. pylinnworks import PyLinnworks
from pylinnworks.api_requests import SKUExists
from pylinnworks.api_requests import GetNewSKU
from pylinnworks.api_requests import AddInventoryItem
from . inventory_search import InventorySearch
from . inventory_view_filter import InventoryViewFilter
from . inventory_item import InventoryItem


class Inventory(PyLinnworks):
    """Provide methods for finding and interacting with inventory items."""

    @classmethod
    def search_inventory(cls, filters=[], locations=None, columns=None):
        """Create inventory search.

        Create instance of `InventorySearch` to allow finding of inventory
        items.

        Args:
            filters (:obj: `list` ('InventoryViewFilter')): `list` containing
                inventory view filters which which the search will be filtered.
            locations (:obj: `list` (`Location`)): `list` containing linnworks
                locations in which to search. If None all locations will be
                searched. Default: None.
            columns (:obj: `list` (`InventoryViewColumn`)): `list` containing
                columns of inventory item data to be returned by the search.
                If None all possible columns will be used. Default: None.

        Returns:
            :obj: InventorySearch: Object providing methods to interact with
                an inventory search.
        """
        return InventorySearch(
            cls, filters=filters, locations=locations, columns=columns)

    @classmethod
    def get_inventory_item(cls, stock_id=None, sku=None):
        """Get inventory item by stock ID (GUID) or SKU.

        Either stock_id or sku kwargs should be supplied. If both are supplied
        sku will take precidence.

        Args:
            stock_id (str): Stock ID (GUID) of item to be returned.
            sku (str): SKU of the item to be returned

        Returns:
            InventoryItem object.
        """
        if stock_id is None and sku is None or stock_id is not None and \
                sku is not None:
            raise ValueError("Either stock_id or sku should be supplied")
        if sku is not None:
            return cls.get_item_by_SKU(sku)
        else:
            return cls.get_item_by_stock_ID(stock_id)

    @classmethod
    def create_new_item(
            cls, stock_id=None, sku=None, title='', barcode=''):
        """Create new inventory item.

        Adds a new item to Linnworks with a Stock ID, SKU, title and barcode.
        All other attributes will use Linnwork's default values. They can be
        set using the returned InventoryItem.

        Args:
            stock_id (str): Stock ID for new item. Must be formatted as a UUID4
                GUID. If not supplied a new one will be generated.
            sku (str): SKU for new item. If not supplied a new SKU will be
                created using get_new_SKU method.
            title (str): Title for new item. Defaults to empty string.
            barcodee (str): Barcode for new item. Defaults to empty string.

        Returns:
            :obj: `InventoryItem` providing attributes and methods for working
                with inventory items.
        """
        if stock_id is None:
            stock_id = uuid.uuid4()
        if sku is None:
            sku = cls.get_new_SKU()
        AddInventoryItem(
            cls, stock_id=stock_id, sku=sku, title=title, barcode=barcode)
        return InventoryItem(cls, stock_id=stock_id)

    @classmethod
    def get_stock_id_by_SKU(cls, sku):
        """Return stock ID (GUID) of item with SKU sku.

        Args:
            sku (str): SKU for which the Stock ID will be found.

        Returns:
            str: Stock ID (GUID) for item with SKU sku.
        """
        item = cls.get_item_by_SKU(sku)
        return item.stock_id

    @classmethod
    def get_new_SKU(cls):
        """Return unused SKU as str.

        Requests a new, unused SKU from linnworks.net API.

        Returns:
            str: Unused SKU.
        """
        return GetNewSKU(cls).response_dict

    @classmethod
    def get_item_by_SKU(cls, sku, locations=None):
        """Return Inventory Item with SKU sku.

        Args:
            sku (str): SKU of item to be found.
            locations (:obj: `list` (`Location`)): `list` containing linnworks
                locations in which to search. If None all locations will be
                searched. Default: None.
        Returns:
            :obj: `InventoryItem`: Inventory item with matching SKU.
        """
        filters = [InventoryViewFilter(
            field='SKU', value=sku)]
        item = InventorySearch(
            cls, filters=filters, locations=locations).get_item()
        return item

    @classmethod
    def search_by_SKU(cls, sku, locations=None):
        """Search inventory by full or partial SKU.

        Args:
            sku (str): SKU of item to be found.
            locations (:obj: `list` (`Location`)): `list` containing linnworks
                locations in which to search. If None all locations will be
                searched. Default: None.
        Returns:
            :obj: `InventoryList`: `InventoryList` containing all inventory
                items who's SKU matches or contains `sku`.
        """
        filters = [InventoryViewFilter(
            filter_name='SKU', field='String', value=sku,
            condition='Contains')]
        inventory_list = InventorySearch(
            cls, filters=filters, locations=locations).get_items()
        return inventory_list

    @classmethod
    def search_by_title(cls, sku, locations=None):
        """Search inventory by full or partial title.

        Args:
            title (str): SKU of item to be found.
            locations (:obj: `list` (`Location`)): `list` containing linnworks
                locations in which to search. If None all locations will be
                searched. Default: None.
        Returns:
            :obj: `InventoryList`: `InventoryList` containing all inventory
                items who's SKU matches or contains `title`.
        """
        filters = [InventoryViewFilter(
            filter_name='Title', field='String', value=sku,
            condition='Contains')]
        inventory_list = InventorySearch(
            cls, filters=filters, locations=locations).get_items()
        return inventory_list

    @classmethod
    def get_item_by_stock_ID(cls, stock_id):
        """Return Inventory Item with stock ID stock_id.

        Args:
            stock_id (str): Stock ID (GUID) of item to be returned

        Returns:
            :obj: `InventoryItem`: `InventoryItem` with matching stock ID.
        """
        return InventoryItem(cls, stock_id=stock_id)

    @classmethod
    def get_inventory_item_count(
            cls, view=None, locations=None, columns=None, filters=None):
        """Return number of items in inventory.

        Creates an inventory search and returns the number of items mathcing
        the search. If no arguments are supplied, returns the total number of
        items in inventory.

        Args:
            filters (:obj: `list` ('InventoryViewFilter')): `list` containing
                inventory view filters which which the search will be filtered.
            locations (:obj: `list` (`Location`)): `list` containing linnworks
                locations in which to search. If None all locations will be
                searched. Default: None.
            columns (:obj: `list` (`InventoryViewColumn`)): `list` containing
                columns of inventory item data to be returned by the search.
                If None all possible columns will be used. Default: None.

        Returns:
            int: Number of inventory items mathcing the search.
        """
        search = InventorySearch(
            cls, view=view, locations=locations, columns=columns,
            filters=filters)
        return search.count_items()

    @classmethod
    def SKU_exists(cls, sku):
        """Check if sku has been used as a product SKU.

        Args:
            sku (str): SKU to check.

        Returns:
            True if SKU belongs to an existing inventory item. Otherwise
                returns False.
        """
        request = SKUExists(cls, sku)
        return request.response_dict

    @classmethod
    def get_inventory(cls, locations=None):
        """Return all inventory.

        Creates an Inventory Search that will match all items and returns
        the items. Can be limited by location.

        Args:
            locations (:obj: `list` (`Location`)): `list` containing linnworks
                locations in which to search. If None all locations will be
                searched. Default: None.
        Returns:
            :obj: `InventoryList`: `InventoryList` containing all inventory
                items matching search.
        """
        return InventorySearch(cls, locations=locations).get_items()
