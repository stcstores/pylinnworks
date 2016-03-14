#!/usr/bin/env python3

"""This module contains the main ``LinnworksAPI`` class, the wrapper class for
the linnworks.net API.
"""

import os
import requests
import json
import uuid
import re
from pprint import pprint

from . inventory_item import InventoryItem as InventoryItem
from . basic_item import BasicItem as BasicItem
from . open_order import OpenOrder as OpenOrder
from . inventory import Inventory as Inventory


class LinnworksAPI:
    """Main wrapper class for linnworks.net API. Allows authentication with
    API and provides methods for many common API requests.
    """

    def __init__(self, username=None, password=None):
        """Authenticate user and set ``self.token`` and ``self.server``
        variables. If password argument is None request password form user as
        ``input()``.

        Keyword Arguments:
            username -- Linnworks username (Default None)
            password -- Linnworks password (Default None)
        """
        self.session = requests.Session()
        if username is None:
            self.username = input('Linnworks Username: ')
        else:
            self.username = username
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

    def get_inventory_items(self, start=0, count=None, view=None):
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
        if count is None:
            count = self.get_item_count()
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
        """
        items = []
        for item_data in response_json['Items']:
            item = self.get_inventory_item_by_id(item_data['Id'])
            items.append(item)
        """
        return response_json

    def get_inventory_list(self, view=None, start=0, count=None):
        """Return *inventory items* as ``inventory.Inventory`` object.

        Keyword arguments:
            start -- Index of first item to be returned. Default 0.
            count -- Number of items to be returned. Default 1.
            view: InventoryView ``JSON`` object to filter results. Default will
                return any item.

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
        view = self.get_new_inventory_view()
        url = self.server + '/api/Inventory/GetInventoryItems'
        view_json = json.dumps(view)
        locations = json.dumps(self.get_location_ids())
        data = {'view': view_json,
                'stockLocationIds': locations,
                'startIndex': 0,
                'itemsCount': 1
                }
        response = self.request(url, data)
        response_json = response.json()
        item_count = response_json['TotalItems']
        return item_count

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
        response = self.get_inventory_items(view=view, count=1)
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
        pprint(view)
        response = self.get_inventory_items(view=view, count=max_count)
        return response

    def search_inventory_item_title(self, title, max_count=None):
        """Returns results of search_inventory_item_title and
        search_variation_group_title as single list
        """
        single_items = self.search_single_inventory_item_title(title,
                                                               max_count)
        variation_groups = self.search_variation_group_title(title, max_count)
        return single_items + variation_groups

    def get_open_order_GUID_by_number(self, order_number):
        """Returns GUID for open order with order number order_number"""
        url = self.server + '/api/Orders/GetOpenOrderIdByOrderOrReferenceId'
        data = {'orderOrReferenceId': order_number, 'filters': json.dumps({})}
        response = self.request(url, data)
        if response.text == 'null':
            return None
        return response.json()

    def process_order_by_GUID(self, guid):
        """Processes order with GUID guid"""
        url = self.server + '/api/Orders/ProcessOrder'
        data = {'orderId': guid, 'scanPerformed': True}
        response = self.request(url, data)
        return response.json()

    def process_order_by_order_number(self, order_number):
        """Processes order wtih order number order_number"""
        guid = self.get_open_order_GUID_by_number(order_number)
        return self.process_order_by_GUID(guid)

    def get_open_order(self, order_number,
                       load_items=True, load_additional_info=False):
        if self.is_guid(order_number):
            order_id = order_number
        else:
            order_id = self.get_open_order_GUID_by_number(order_number)
        url = self.server + '/api/Orders/GetOrder'
        data = {}
        data['orderId'] = order_id
        data['fulfilmentLocationId'] = self.get_location_ids()[0]
        data['loadItems'] = load_items
        data['loadAdditionalInfo'] = load_additional_info
        response = self.request(url, data)
        return OpenOrder(response.json())

    def order_is_printed(self, order_number):
        if self.is_guid(order_number):
            order_id = order_number
        else:
            order_id = self.get_open_order_GUID_by_number(order_number)
        order_info = self.get_order_data(order_id)
        return order_info['GeneralInfo']['InvoicePrinted']

    def is_guid(self, guid):
        regex = re.compile(('^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab]'
                            '[a-f0-9]{3}-?[a-f0-9]{12}\Z'), re.I)
        match = regex.match(guid)
        return bool(match)

    def get_open_order_ids(self):
        url = self.server + '/api/Orders/GetAllOpenOrders'
        data = {}
        data['filters'] = {}
        data['fulfilmentCenter'] = self.get_location_ids()[0]
        data['additionalFilter'] = ''
        response = self.request(url, data)
        return response.json()

    def count_open_orders(self):
        order_ids = self.get_open_order_ids()
        return len(order_ids)

    def get_open_orders(self):
        order_count = self.count_open_orders()
        url = self.server + '/api/Orders/GetOpenOrders'
        data = {}
        data['entriesPerPage'] = order_count
        data['pageNumber'] = '1'
        data['filters'] = {}
        data['fulfilmentCenter'] = self.get_location_ids()[0]
        data['additionalFilter'] = ''
        response = self.request(url, data)
        orders = []
        for order_data in response.json()['Data']:
            orders.append(OpenOrder(order_data))
        return orders

    def update_bin_rack(self, item, value,
        location='00000000-0000-0000-0000-000000000000'):
        url = self.server + '/api/Inventory/UpdateInventoryItemLocationField'
        if self.is_guid(item):
            guid = item
        else:
            guid = self.get_inventory_item_id_by_SKU(item)
        data = {
            'fieldName': 'BinRack',
            'fieldValue': str(value),
            'inventoryItemId': guid,
            'locationId': location
        }
        return self.request(url, data)

    def update_category(self, item, category):
        url = self.server + '/api/Inventory/UpdateInventoryItemField'
        if self.is_guid(item):
            guid = item
        else:
            guid = self.get_inventory_item_id_by_SKU(item)
        if self.is_guid(category):
            category_id = category
        else:
            category_id = self.get_category_id(category)
        data = {
            'fieldName': 'Category',
            'fieldValue': category_id,
            'inventoryItemId': guid,
        }
        return self.request(url, data)
