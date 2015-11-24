#!/usr/bin/env python3

"""This module contains the main ``LinnworksAPI`` class, the wrapper class for
the linnworks.net API.
"""

import os
import requests
import json
import uuid

from . inventory_item import InventoryItem as InventoryItem
from . inventory import Inventory as Inventory


class LinnworksAPI:
    """Main wrapper class for linnworks.net API. Allows authentication with
    API and provides methods for many common API requests.
    """

    def __init__(self, password=None):
        """Authenticate user and set ``self.token`` and ``self.server``
        variables. If password argument is None request password form user as
        ``input()``.

        Keyword Arguments:
            username -- Linnworks username (Default None)
            password -- Linnworks password (Default None)
        """
        self.session = requests.Session()
        self.username = 'stcstores@yahoo.com'
        if password is None:
            self.password = input('Linnworks Password: ')
        else:
            self.password = password
        self.get_token()

    def make_request(self, url, data=None, params=None, files=None):
        """Request resource URL

        Arguments:
            url -- URL of resource to be requested.

        Keyword arguments:
            data --  dict containing POST request variables. (Default None)
            params --  dict containing GET request variables. (Default None)

        Returns:
            ``requests.Request`` object.
        """
        response = self.session.post(
            url, data=data, params=params, files=files)
        return response

    def request(self, url, data=None, params={}, files=None):
        """Add authentication variables and make API request.

        Arguments:
            url -- URL to request.

        Keyword Arguments:
            data -- ``dict`` of GET variables (Default None)

        Returns:
            ``requests.Request`` object.
        """
        params['token'] = self.token
        return self.make_request(url, data=data, params=params, files=files)

    def get_token(self):
        """Make authentication requests and set ``self.token`` and
        ``self.server`` accordingly.
        """
        login_url = 'https://api.linnworks.net//api/Auth/Multilogin'
        auth_url = 'https://api.linnworks.net//api/Auth/Authorize'
        login_data = {'userName': self.username, 'password': self.password}
        multilogin = self.make_request(login_url, login_data).json()
        self.user_id = multilogin[0]['Id']
        auth_data = login_data
        auth_data['userId'] = self.user_id
        authorize = self.make_request(auth_url, auth_data).json()
        self.token = authorize['Token']
        self.server = authorize['Server']

    def create_guid(self):
        """Return new ``GUID``."""
        return str(uuid.uuid4())

    def get_category_info(self):
        """Return *category* information as ``dict``."""
        url = self.server + '/api/Inventory/GetCategories'
        response = self.request(url)
        response_json = response.json()
        categories = []
        for category in response_json:
            new_category = {}
            new_category['name'] = category['CategoryName']
            new_category['id'] = category['CategoryId']
            categories.append(new_category)
        return categories

    def get_category_names(self):
        """Return *category* names as ``list``."""
        category_names = []
        for category in self.get_category_info():
            category_names.append(category['name'])
        return category_names

    def get_category_ids(self):
        """Return *category* IDs as ``list``."""
        category_ids = []
        for category in self.get_category_info():
            category_ids.append(category['id'])
        return category_ids

    def get_packaging_group_info(self):
        """Return *packaging group* information as ``dict``."""
        url = self.server + '/api/Inventory/GetPackageGroups'
        response = self.request(url)
        response_json = response.json()
        packaging_groups = []
        for group in response_json:
            new_group = {}
            new_group['id'] = group['Value']
            new_group['name'] = group['Key']
            packaging_groups.append(new_group)
        return packaging_groups

    def get_packaging_group_names(self):
        """Return *packaging group* names as ``list``."""
        packaging_group_names = []
        for group in self.get_packaging_group_info():
            packaging_group_names.append(group['name'])
        return packaging_group_names

    def get_shipping_method_info(self):
        """Return *shipping method* information and return as ``dict``."""
        url = self.server + '/api/Orders/GetShippingMethods'
        response = self.request(url)
        response_json = response.json()
        shipping_methods = []
        for service in response_json:
            for method in service['PostalServices']:
                new_method = {}
                new_method['vendor'] = method['Vendor']
                new_method['id'] = method['pkPostalServiceId']
                new_method['tracking_required'] = method[
                    'TrackingNumberRequired']
                new_method['name'] = method['PostalServiceName']
                shipping_methods.append(new_method)
        return shipping_methods

    def get_shipping_method_names(self):
        """Return *shipping method* as ``list``."""
        shipping_group_names = []
        for group in self.get_shipping_method_info():
            shipping_group_names.append(group['name'])
        return shipping_group_names

    def get_location_info(self):
        """Return *location* names and IDs and return as ``dict``."""
        url = self.server + '/api/Inventory/GetStockLocations'
        response = self.request(url)
        response_json = response.json()
        locations = []
        for location in response_json:
            new_location = {}
            new_location['name'] = location['LocationName']
            new_location['id'] = location['StockLocationId']
            locations.append(new_location)
        return locations

    def get_location_names(self):
        """Return *location* names as ``list``."""
        locations = []
        for location in self.get_location_info():
            locations.append(location['name'])
        return locations

    def get_location_ids(self):
        """Return *location* IDs as ``list``."""
        locations = []
        for location in self.get_location_info():
            locations.append(location['id'])
        return locations

    def get_postage_service_info(self):
        """Return *postage service* names and IDs and return as ``dict``."""
        url = self.server + '/api/PostalServices/GetPostalServices'
        response = self.request(url)
        response_json = response.json()
        postage_services = []
        for postage_service in response_json:
            new_service = {}
            new_service['name'] = postage_service['PostalServiceName']
            new_service['id'] = postage_service['pkPostalServiceId']
            postage_services.append(new_service)
        return postage_services

    def get_postage_service_names(self):
        """Return *postage service* names as ``list``."""
        postage_services = []
        for postage_service in self.get_postage_service_info():
            postage_services.append(postage_service['name'])
        return postage_services

    def get_postage_service_ids(self):
        """Return *postage service* IDs as ``list``."""
        postage_services = []
        for postage_service in self.get_postage_service_info():
            postage_services.append(postage_service['id'])
        return postage_services

    def get_channels(self):
        """Return *channel* information as ``dict``."""
        url = self.server + '/api/Inventory/GetChannels'
        response = self.request(url)
        response_json = response.json()
        channels = []
        for channel in response_json:
            channels.append(channel['Source'] + ' ' + channel['SubSource'])
        return channels

    def get_inventory_views(self):
        """Return ``list`` of *inventory views*."""
        url = self.server + '/api/Inventory/GetInventoryViews'
        response = self.request(url)
        response_json = response.json()
        return response_json

    def get_new_inventory_view(self):
        """Returns default *inventory view*."""
        url = self.server + '/api/Inventory/GetNewInventoryView'
        response = self.request(url)
        response_json = response.json()
        return response_json

    def get_inventory_column_types(self):
        """Return ``list`` of *column types*."""
        url = self.server + '/api/Inventory/GetInventoryColumnTypes'
        response = self.request(url)
        return response

    def get_inventory_items(self, start=0, count=1, view=None):
        """Rquest *inventory items*.

        Keyword arguments:
            start -- Index of first item to be returned. Default 0.
            count -- Number of items to be returned. Default 1.
            view: InventoryView ``JSON`` object to filter results. Default will
                return any item.

        Returns:
            ``requests.Request`` object.
        """
        if view is None:
            view = self.get_new_inventory_view()
        url = self.server + '/api/Inventory/GetInventoryItems'
        view_json = json.dumps(view)
        locations = json.dumps(self.get_location_ids())
        data = {'view': view_json,
                'stockLocationIds': locations,
                'startIndex': start,
                'itemsCount': count
                }
        response = self.request(url, data)
        response_json = response.json()
        return response_json

    def get_inventory_list(self, view=None, start=0, count=None):
        """Return *inventory items* as ``inventory.Inventory`` object.

        Keyword arguments:
            start -- Index of first item to be returned. Default 0.
            count -- Number of items to be returned. Default 1.
            view: InventoryView ``JSON`` object to filter results. Default will
                return any item.
            to_json -- If True method returns parsed JSON. (Default True)

        Returns:
            ``inventory.Inventory`` object.
        """
        if view is None:
            view = self.get_new_inventory_view()
        if count is None:
            item_count = self.get_item_count()
        else:
            item_count = count
        item_list = self.get_inventory_items(start=start,
                                             count=item_count,
                                             view=view)['Items']
        inventory = Inventory(item_list, self)
        return inventory

    def get_item_count(self):
        """Return number of items in *inventory*."""
        request = self.get_inventory_items(start=0, count=1, view=None)
        item_count = request['TotalItems']
        return item_count

    def get_inventory_item_by_id(self, stock_id, inventory_item=True):
        """Returns **inventory item** data for the item with the specifed
        *stock id*.

        Arguments:
            stock_id -- GUID of *inventory item*.

        Keyword Arguments:
            inventory_item -- If true return ``inventory_item.InventoryItem``.
                Else return parsed ``JSON``.

        Returns:
            If inventory_item is True returns ``inventory_item.InventoryItem``.
            Else Parsed ``JSON``.
        """
        url = self.server + '/api/Inventory/GetInventoryItemById'
        data = {'id': stock_id}
        response = self.request(url, data).json()
        if inventory_item is not True:
            return response
        else:
            item = InventoryItem(self, stock_id)
            item.sku = response['ItemNumber']
            item.title = response['ItemTitle']
            item.purchase_price = response['PurchasePrice']
            item.retail_price = response['RetailPrice']
            item.barcode = response['BarcodeNumber']
            item.category_id = response['CategoryId']
            item.depth = response['Depth']
            item.height = response['Height']
            item.package_group_id = response['PackageGroupId']
            item.postage_service_id = response['PostalServiceId']
            item.tax_rate = response['TaxRate']
            item.variation_group_name = response['VariationGroupName']
            item.weight = response['Weight']
            item.width = response['Width']
            item.meta_data = response['MetaData']
            item.quantity = self.get_stock_level_by_id(stock_id)
            for category in self.get_category_info():
                if category['id'] == item.category_id:
                    item.category = category['name']
            for package_group in self.get_packaging_group_info():
                if package_group['id'] == item.package_group_id:
                    item.package_group = package_group['name']
            for postage_service in self.get_shipping_method_info():
                if postage_service['id'] == item.postage_service:
                    item.postage_service = postage_service['name']
            return item

    def get_extended_property_names(self):
        """Return ``list`` of *extended property* names."""
        url = self.server + '/api/Inventory/GetExtendedPropertyNames'
        response = self.request(url)
        response_json = response.json()
        return response_json

    def get_inventory_item_extended_properties(self, stock_id):
        """Return ``dict`` of *extended properties* names and IDs.

        Arguments:
            stock_id -- GUID of *inventory item*.
        """
        url = self.server + '/api/Inventory/GetInventoryItemExtendedProperties'
        data = {'inventoryItemId': stock_id}
        response = self.request(url, data)
        response_json = response.json()
        return response_json

    def get_new_sku(self):
        """Return unsed product SKU."""
        url = self.server + '/api/Stock/GetNewSKU'
        response = self.request(url)
        response_json = response.json()
        return response_json

    def sku_exists(self, sku):
        """Return True if sku exists for item on Linnworks server."""
        url = self.server + '/api/Stock/SKUExists'
        data = {'SKU': sku}
        response = self.request(url, data)
        response_json = response.json()
        return response_json

    def upload_image(self, filepath):
        """Upload image file to Linnworks Server.

        Arguments:
            filename -- Filename for the image.
            filepath -- Full path to the image.

        Returns:
            Server response as parsed JSON. This contains the id assigned to
            the image. This must be used to apply the image to a product.
        """
        filename = os.path.basename(filepath)
        url = self.server + '/api/Uploader/UploadFile'
        params = {'type': 'Image', 'expiredInHours': '24'}
        files = {filename: open(filepath, 'rb')}
        response = self.request(url, params=params, files=files)
        response_json = response.json()
        return response_json

    def create_variation_group(self, parent_title, variation_guids,
                               parent_guid=None, parent_sku=None):
        """Create a variation group.

        Arguments:
            parent_title -- Title of new variation group.
            variation_guids -- List of variation group products *stock_ids*.

        Keyword Arguments:
            parent_guid -- New guid to be used as pkVariationId. Creates one by
                default.
            parent_sku -- New SKU for the new variation group. Creates one by
                default.

        Returns:
            True if server response is empty string. Otherwise returns the
            server response.
        """
        if parent_guid is None:
            parent_guid = self.create_guid()
        if parent_sku is None:
            parent_sku = self.get_new_sku()
        url = self.server + '/api/Stock/CreateVariationGroup'
        template = {}
        template['ParentSKU'] = parent_sku
        template['VariationGroupName'] = parent_title
        template['ParentStockItemId'] = parent_guid
        template['VariationItemIds'] = variation_guids
        data = {'template': json.dumps(template)}
        response = self.request(url, data)
        if response.text == '':
            return True
        else:
            return response

    def get_variation_group_id_by_SKU(self, sku):
        """Return *stock id* for *variation group* with SKU ``sku``."""
        url = self.server + '/api/Stock/SearchVariationGroups'
        data = {}
        data['searchText'] = str(sku)
        data['searchType'] = 'ParentSKU'
        data['entriesPerPage'] = '100'
        data['pageNumber'] = 1
        response = self.request(url, data)
        response_json = response.json()
        return response_json['Data'][0]['pkVariationItemId']

    def get_variation_group_inventory_item_by_SKU(self, sku):
        """Return ``inventory_item.InventoryItem`` containing *variation group*
        with SKU ``sku``.
        """
        guid = self.get_variation_group_id_by_SKU(sku)
        item = self.get_inventory_item_by_id(guid)
        return item

    def get_inventory_item_id_by_SKU(self, sku):
        """Return *stock id* for *inventory item* with SKU ``sku``."""
        view = self.get_new_inventory_view()
        view['Columns'] = []
        _filter = {}
        _filter['Value'] = str(sku)
        _filter['Field'] = 'String'
        _filter['FilterName'] = 'SKU'
        _filter['FilterNameExact'] = ''
        _filter['Condition'] = 'Equals'
        view['Filters'] = [_filter]
        response = self.get_inventory_items(view=view)
        stock_id = response['Items'][0]['Id']
        return stock_id

    def get_inventory_item_by_SKU(self, sku):
        """Return ``inventory_item.InventoryItem`` containing *inventory item*
        with SKU ``sku``.
        """
        guid = self.get_inventory_item_id_by_SKU(sku)
        item = self.get_inventory_item_by_id(guid)
        return item

    def get_all_open_order_ids(self, filters={}):
        """Return list containing **order guid** for all current **open orders**

        Keyword Arguments:
            filters **filter** object as ''dict''. Defaults to empty ''dict''.
        """
        fulfilment_center = '00000000-0000-0000-0000-000000000000'
        for location in self.get_location_info():
            if location['name'] == 'Default':
                fulfilment_center = location['id']

        data = {'filters': json.dumps('{}'),
                'fulfilmentCenter': fulfilment_center,
                'additionalFilter': ''}
        url = self.server + '/api/Orders/GetAllOpenOrders'
        response = self.request(url, data)
        order_ids = response.json()
        return order_ids

    def get_all_open_orders(self, filters={}):
        order_ids = self.get_all_open_order_ids(filters=filters)
        fulfilment_location_id = '00000000-0000-0000-0000-000000000000'
        for location in self.get_location_info():
            if location['name'] == 'Default':
                fulfilment_location_id = location['id']
        data = {'ordersIds': json.dumps(order_ids),
                'fulfilmentLocationId': fulfilment_location_id,
                'loadItems': 'true',
                'loadAdditionalInfo': 'true'}
        url = self.server + '/api/Orders/GetOrders'
        response = self.request(url, data)
        return response.json()

    def get_image_urls_by_item_id(self, item_id):
        url = self.server + '/api/Inventory/GetInventoryItemImages'
        data = {'inventoryItemId': item_id}
        response = self.request(url, data)
        response_json = response.json()
        image_urls = []
        for image in response_json:
            if image['IsMain'] is True:
                image_url = image['Source'].replace('tumbnail_', '')
                image_urls.append(image_url)
        for image in response_json:
            if image['IsMain'] is not True:
                image_url = image['Source'].replace('tumbnail_', '')
                image_urls.append(image_url)
        return image_urls

    def get_image_urls_by_SKU(self, sku):
        item_id = self.get_inventory_item_id_by_SKU(sku)
        image_urls = self.get_image_urls_by_item_id(item_id)
        return image_urls

    def get_stock_level_by_id(self, stock_id, location='Default'):
        url = self.server + '/api/Stock/GetStockLevel'
        data = {'stockItemId': stock_id}
        response = self.request(url, data)
        for loc in response.json():
            if loc['Location']['LocationName'] == location:
                return loc['Available']
        raise Exception('Location Not Valid')

    def get_stock_level_by_SKU(self, sku, location='Default'):
        stock_id = self.get_inventory_item_id_by_SKU(sku)
        return self.get_stock_level_by_id(stock_id, location)

    def get_channel_titles(self, guid):
        url = self.server + '/api/Inventory/GetInventoryItemTitles'
        data = {'inventoryItemId': guid}
        response = self.request(url, data)
        response_json = response.json()
        channels = {}
        for channel in response_json:
            if channel['Source'] == 'AMAZON':
                if channel['SubSource'] == 'Stc Stores':
                    channels['amazon'] = channel['Title']
            elif channel['Source'] == 'EBAY':
                if channel['SubSource'] == 'EBAY0':
                    channels['ebay'] = channel['Title']
            elif channel['Source'] == 'SHOPIFY':
                if channel['SubSource'] == 'stcstores.co.uk (shopify)':
                    channels['shopify'] = channel['Title']
        return channels

    def get_channel_prices(self, guid):
        url = self.server + '/api/Inventory/GetInventoryItemPrices'
        data = {'inventoryItemId': guid}
        response = self.request(url, data)
        response_json = response.json()
        channels = {}
        for channel in response_json:
            if channel['Source'] == 'AMAZON':
                if channel['SubSource'] == 'Stc Stores':
                    channels['amazon'] = channel['Price']
            elif channel['Source'] == 'EBAY':
                if channel['SubSource'] == 'EBAY0':
                    channels['ebay'] = channel['Price']
            elif channel['Source'] == 'SHOPIFY':
                if channel['SubSource'] == 'stcstores.co.uk (shopify)':
                    channels['shopify'] = channel['Price']
        return channels

    def get_channel_descriptions(self, guid):
        url = self.server + '/api/Inventory/GetInventoryItemTitles'
        data = {'inventoryItemId': guid}
        response = self.request(url, data)
        response_json = response.json()
        channels = {}
        for channel in response_json:
            if channel['Source'] == 'AMAZON':
                if channel['SubSource'] == 'Stc Stores':
                    channels['amazon'] = channel['Description']
            elif channel['Source'] == 'EBAY':
                if channel['SubSource'] == 'EBAY0':
                    channels['ebay'] = channel['Description']
            elif channel['Source'] == 'SHOPIFY':
                if channel['SubSource'] == 'stcstores.co.uk (shopify)':
                    channels['shopify'] = channel['Description']
        return channels

    def get_variation_children(self, parent_guid):
        """Return list of GUIDs for variations in the variation group with
        specified GUID
        """
        url = self.server + '/api/Stock/GetVariationItems'
        data = {'pkVariationItemId': parent_guid}
        response = self.request(url, data)
        response_json = response.json()
        variation_children = []
        for child in response_json:
            variation_children.append(child['pkStockItemId'])
        return variation_children

    def make_inventory_search_filter(self, value, filter_name, condition):
        """Returns filter object for use with inventory view object"""
        _filter = {}
        _filter['Value'] = str(value)
        _filter['Field'] = 'String'
        _filter['FilterName'] = filter_name
        _filter['FilterNameExact'] = ''
        _filter['Condition'] = condition
        return _filter

    def get_inventory_search_columns(self):
        """Returns columns object for use with inventory view object.
        Uses columns SKU and Title
        """
        columns = [
            {"ColumnName": "SKU",
                "DisplayName": "SKU",
                "Group": "General",
                "Field": "String",
                "SortDirection": "None",
                "Width": 150,
                "IsEditable": False},
            {"ColumnName": "Title",
                "DisplayName": "Title",
                "Group": "General",
                "Field": "String",
                "SortDirection": "None",
                "Width": 250,
                "IsEditable": True}]
        return columns

    def search_variation_group_title(self, title, max_count=None):
        """Return list of dictionaries with title, sku and guid of variation
        groups where their title contains passed title.
        """
        if max_count is None:
            max_count = self.get_item_count()
        url = self.server + '/api/Stock/SearchVariationGroups'
        data = {
            'searchType': 'VariationName',
            'searchText': str(title),
            'pageNumber': 1,
            'entriesPerPage': max_count
        }
        response = self.request(url, data).json()
        variation_groups = []
        for group in response['Data']:
            new_group = {}
            new_group['guid'] = group['pkVariationItemId']
            new_group['sku'] = group['VariationSKU']
            new_group['title'] = group['VariationGroupName']
            new_group['variation_group'] = True
            variation_groups.append(new_group)
        return variation_groups

    def search_single_inventory_item_title(self, title, max_count=None):
        """Return list of dictionaries with title, sku and guid of inventory
        items where their title contains passed title.
        """
        if max_count is None:
            max_count = self.get_item_count()
        view = self.get_new_inventory_view()
        view['Columns'] = self.get_inventory_search_columns()
        view_filter = self.make_inventory_search_filter(title,
                                                        'Title',
                                                        'Contains')
        view['Filters'] = [view_filter]
        response = self.get_inventory_items(view=view, count=max_count)
        items = []
        for item in response['Items']:
            new_item = {}
            new_item['guid'] = item['Id']
            new_item['sku'] = item['SKU']
            new_item['title'] = item['Title']
            new_item['variation_group'] = False
            items.append(new_item)
        return items

    def search_inventory_item_title(self, title, max_count=None):
        """Returns results of search_inventory_item_title and
        search_variation_group_title as single list
        """
        single_items = self.search_single_inventory_item_title(title,
                                                               max_count)
        variation_groups = self.search_variation_group_title(title, max_count)
        return single_items + variation_groups
