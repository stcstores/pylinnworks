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

    def get_stock_level_by_id(self, stock_id, location='Default'):
        url = self.server + '/api/Stock/GetStockLevel'
        data = {'stockItemId': stock_id}
        response = self.request(url, data)
        for loc in response.json():
            if loc['Location']['LocationName'] == location:
                return loc['Available']
        raise Exception('Location Not Valid')

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
