import requests
import json
from pprint import pprint

from . inventory_item import InventoryItem as InventoryItem
from . inventory import Inventory as Inventory

class LinnworksAPI:

    
    def __init__(self, password=None):
        """Object with methods to simplify calls to linnworks.net API.
        
        Args:
            password (str): User password. If not provided as argument it will
            be requesed as an input().
        """
        self.session = requests.Session()
        self.username = 'stcstores@yahoo.com'
        if password == None:
            self.password = input('Linnworks Password: ')
        else:
            self.password = password
        self.get_token()
        

    def make_request(self, url, data=None, to_json=True):
        """Requests resource URL with GET variables specified in data.
        
        Args:
            url (str): URL of resource to be requested.
            data (dict): Key value pairs for GET request variables
            to_json(bool): If True True a requests.request object
                will be returned. Otherwise will return the response as parsed JSON.
                
        Returns:
            If to_json is True returns response as parsed JSON. Otherwise returns
            requests.Request object.
        """
        response = self.session.get(url, params=data)
        if to_json == True:
            return response.json()
        else:
            return response
        

    def request(self, url, data=None, to_json=True):
        """Adds self.token to data and calls self.make_request(url, data, to_json).
        
        Args:
            url (str): URL to be passed to self.make_request().
            data (dict): GET variables to be passed to self.make_request().
            to_json (bool): Passed as to_json argument to self.make_request().
            
        Returns:
            Returns the return from call to self.make_request().
        """
        if data == None:
            data = {}
        data['token'] = self.token
        return self.make_request(url, data, to_json=to_json)
    

    def get_token(self):
        """Makes API request to get token and server url. Sets self.token and
        self.server accordingly.
        """
        login_url = 'https://api.linnworks.net//api/Auth/Multilogin'
        auth_url =  'https://api.linnworks.net//api/Auth/Authorize'
        login_data = {'userName' : self.username, 'password' : self.password}
        multilogin = self.make_request(login_url, login_data)
        self.user_id = multilogin[0]['Id']
        auth_data = login_data
        auth_data['userId'] = self.user_id
        authorize = self.make_request(auth_url, auth_data)
        self.token = authorize['Token']
        self.server = authorize['Server']
        

    def get_category_info(self):
        """Makes API call to get category information and returns a list
        containg a dict of each categorys name and id.
        
        Returns:
            list containing categories as dict containing 'name' and 'id'.
        """
        url = self.server + '/api/Inventory/GetCategories'
        response = self.request(url)
        categories = []
        for category in response:
            new_category = {}
            new_category['name'] = category['CategoryName']
            new_category['id'] = category['CategoryId']
            categories.append(new_category)
        return categories
    

    def get_category_names(self):
        """Returns:
            list containing the name of each category.
        """
        category_names = []
        for category in self.get_category_info():
            category_names.append(category['name'])
        return category_names
    

    def get_category_ids(self):
        """Returns:
            list containing the id of each category
        """
        category_ids = []
        for category in self.get_category_info():
            category_ids.append(category['id'])
        return category_ids
    
    
    def get_packaging_group_info(self):
        """Makes API call to get packaging group information and returns a list
        containg a dict of each categorys name and id.
        
        Returns:
            list containing packaging groups as dict containing 'name' and 'id'.
        """
        url = self.server + '/api/Inventory/GetPackageGroups'
        response = self.request(url)
        packaging_groups = []
        for group in response:
            new_group = {}
            new_group['id'] = group['Value']
            new_group['name'] = group['Key']
            packaging_groups.append(new_group)
        return packaging_groups
    
    
    def get_packaging_group_names(self):
        """Returns:
            list containing the name of each packaging group.
        """
        packaging_group_names = []
        for group in self.get_packaging_group_info():
            packaging_group_names.append(group['name'])
        return packaging_group_names
    
    
    def get_shipping_method_info(self):
        """Makes API call to get shipping method information and returns a list
        containg a dict of each categorys name and id.
        
        Returns:
            list containing shipping method as dict containing 'name' and 'id'.
        """
        url = self.server + '/api/Orders/GetShippingMethods'
        response = self.request(url)
        shipping_methods = []
        for service in response:
            for method in service['PostalServices']:
                new_method = {}
                new_method['vendor'] = method['Vendor']
                new_method['id'] = method['pkPostalServiceId']
                new_method['tracking_required'] = method['TrackingNumberRequired']
                new_method['name'] = method['PostalServiceName']
                shipping_methods.append(new_method)
        return shipping_methods
    
    
    def get_shipping_method_names(self, ):
        """Returns:
            list containing the name of each shipping method.
        """
        shipping_group_names = []
        for group in self.get_shipping_method_info():
            shipping_group_names.append(group['name'])
        return shipping_group_names
    
    
    def get_location_info(self):
        """Makes API call to get location information and returns a list
        containg a dict of each categorys name and id.
        
        Returns:
            list containing location as dict containing 'name' and 'id'.
        """
        url = self.server + '/api/Inventory/GetStockLocations'
        response = self.request(url)
        locations = []
        for location in response:
            new_location = {}
            new_location['name'] = location['LocationName']
            new_location['id'] = location['StockLocationId']
            locations.append(new_location)
        return locations
    
    
    def get_location_names(self):
        """Returns:
            list containing the name of each location.
        """
        locations = []
        for location in self.get_location_info():
            locations.append(location['name'])
        return locations
    

    def get_location_ids(self):
        """Returns:
            list containing the id of each location.
        """
        locations = []
        for location in self.get_location_info():
            locations.append(location['id'])
        return locations
    

    def get_channels(self):
        """Returns:
            list containing all channels.
        """
        url = self.server + '/api/Inventory/GetChannels'
        response = self.request(url)
        channels = []
        for channel in response:
            channels.append(channel['Source'] + ' ' + channel['SubSource'])
        return channels


    def get_inventory_views(self):
        """Returns:
            Response to API call to GetInventoryViews as parsed JSON.
        """
        url = self.server + '/api/Inventory/GetInventoryViews'
        response = self.request(url)
        return response
    

    def get_new_inventory_view(self):
        """Returns:
            Inventory View for use with calls to GetInventory.
        """
        url = self.server + '/api/Inventory/GetNewInventoryView'
        response = self.request(url, to_json=to_json)
        return response
    

    def get_inventory_column_types(self):
        """Returns:
            Response to API call to GetInventoryColumnTypes as parsed JSON.
        """
        url = self.server + '/api/Inventory/GetInventoryColumnTypes'
        response = self.request(url, to_json=to_json)
        return response
    

    def get_inventory_items(self, start=0, count=1, to_json=True, view=None):
        """Makes request to GetInventoryItems.
        
        Args:
            start (int): Index of first item to be returned.
            count (int): Number of items to be returned.
            view: InventoryView dictionary object. Defaults to new inventory view
                from self.get_new_inventory_view().
        
        Returns:
            List of items. Which items this list contains and what info about
                them is included depends on the InventoryView
        """
        url = self.server + '/api/Inventory/GetInventoryItems'
        if view == None:
            view = json.dumps(self.get_new_inventory_view())
        else:
            view = json.dumps(view)
        locations = json.dumps(self.get_location_ids())
        data = {'view' : view,
                'stockLocationIds' : locations,
                'startIndex' : start,
                'itemsCount' : count
                }
        response = self.request(url, data, to_json=to_json)
        return response
    

    def get_inventory_list(self, view=None, start=0, count=None):
        """Calls self.get_inventory_items() and Inventory() object for the
        returned items.
        
        Args:
            view: InventoryView to be passed to call to self.get_inventory_items().
            start: Passed to self.get_inventory_items() as start argument.
            count: Passed to self.get_inventory_items() as count argument.
        
        Returns:
            Invntory() object.
        """
        if count == None:
            item_count = self.get_item_count()
        else:
            item_count = count
        
        all_items = []
        item_list =  self.get_inventory_items(start=start,
                count=item_count, view=view)['Items']
        
        inventory = Inventory(item_list, self)
        return inventory
    
    
    def get_item_count(self):
        """Returns:
            Number of items in inventory as int.
        """
        request = self.get_inventory_items(start=0, count=1, view=None)
        item_count = request['TotalItems']
        return item_count
        
        
    def get_inventory_item_by_id(self, stock_id, inventory_item=True):
        """Returns inventory item data for the item with the specifed stock id.
        
        Returns:
            If inventory_item is True returns InventoryItem() else returns dict.
        """
        url = self.server + '/api/Inventory/GetInventoryItemById'
        data = {'id' : stock_id}
        response = self.request(url, data)
        if inventory_item != True:
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
            item.quantity = response['Quantity']
            item.meta_data = response['MetaData']
            
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
        """Returns:
            list containing names of extended properties.
        """
        url = self.server + '/api/Inventory/GetExtendedPropertyNames'
        response = self.request(url)
        return response
    

    def get_inventory_item_extended_properties(self, stock_id):
        """Returns:
            dict of extended properties for item with passed stock id.
        """
        url = self.server + '/api/Inventory/GetInventoryItemExtendedProperties'
        data = {'inventoryItemId' : stock_id}
        response = self.request(url, data)
        return response
    
    
    def get_new_sku(self):
        """Returns:
            Unsed product SKU.
        """
        url = self.server + '/api/Stock/GetNewSKU'
        response = self.request(url)
        return response
    
    
    def sku_exists(self, sku):
        """Returns:
            True if the passed SKU is used for an inventory item. Otherwise False.
        """
        url = self.server + '/api/Stock/SKUExists'
        data = {'SKU' : sku}
        response = self.request(url, data)
        return response
    
    
    def upload_image(self, filename, filepath):
        """Uploads an image file to Linnworks Server.
        
        Args:
            filename (str): Filename for the image.
            filepath (str): Full path to the image.
            
        Returns:
            Server response as parsed JSON. This contains the id assigned to the
            image. This must be used to apply the image to a product.
        """
        url = self.server + '/api/Uploader/UploadFile?type=Image&expiredInHours=24&token='
        url += self.token
        files = {filename : open(filepath, 'rb')}
        response = self.session.post(url, files=files)
        return response
    
    
    def create_variation_group(self, parent_guid, parent_sku, parent_title, variation_guids):
        """Creates a variation group.
        
        Args:
            parent_guid (str): New guid to be used as pkVariationId.
            parent_sku (str): New SKU for the new variation group.
            parent_title (str): Title of new variation group.
            variation_guids (list<str(guid)>): List of variation group products
                stock_ids.
                
        Returns:
            Server response as parsed JSON.
        """
        url = self.server + '/api/Stock/CreateVariationGroup'
        template = {}
        template['ParentSKU'] = parent_sku
        template['VariationGroupName'] = parent_title
        template['ParentStockItemId'] = parent_guid
        template['VariationItemIds'] = variation_guids
        data = {'template' : json.dumps(template)}
        response = self.request(url, data)
        return response
    
    
    def get_variation_group_guid_by_SKU(self, sku):
        """Returns:
            stock_id of variation group parent with passed sku.
        """
        url = self.server + '/api/Stock/SearchVariationGroups'
        data = {}
        data['searchText'] = str(sku)
        data['searchType'] = 'ParentSKU'
        data['entriesPerPage'] = '100'
        data['pageNumber'] = 1
        response = self.request(url, data)
        print(response)
        return response['Data'][0]['pkVariationItemId']
    
        
    def get_variation_group_inventory_item_by_SKU(self, sku):
        """Returns:
            InventoryItem() of variation group parent with passed sku.
        """
        guid = self.get_variation_group_guid_by_SKU(sku)
        item = self.get_inventory_item_by_id(guid)
        return item
    
    
    def get_item_stock_id_by_SKU(self, sku):
        """Returns:
            stock_id of item with the passed sku.
        """
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
        """Returns:
            InventroyItem() for item with passed sku.
        """
        guid = self.get_item_stock_id_by_SKU(sku)
        item = self.get_inventory_item_by_id(guid)
        return item