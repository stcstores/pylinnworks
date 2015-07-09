import requests
import json
from pprint import pprint

from inventory_item import InventoryItem as InventoryItem

class LinnworksAPI:

    
    def __init__(self):
        self.username = 'stcstores@yahoo.com'
        self.password = input('Linnworks Password: ')
        self.get_token()

    def make_request(self, url, data=None, to_json=True):
        response = requests.get(url, params=data)
        #print(request.url)
        #print(request.text)
        #pprint(parsed_json)
        if to_json == True:
            return response.json()
        else:
            return response

    def request(self, url, data=None, to_json=True):
        if data == None:
            data = {}
        data['token'] = self.token
        return self.make_request(url, data, to_json=to_json)

    def get_token(self):
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

    def get_category_info(self, to_json=True):
        url = self.server + '/api/Inventory/GetCategories'
        response = self.request(url, to_json=to_json)
        categories = []
        for category in response:
            new_category = {}
            new_category['name'] = category['CategoryName']
            new_category['id'] = category['CategoryId']
            categories.append(new_category)
        return categories

    def get_category_names(self):
        category_names = []
        for category in self.get_category_info():
            category_names.append(category['name'])
        return category_names

    def get_category_ids(self):
        category_ids = []
        for category in self.get_category_info():
            category_ids.append(category['id'])
        return category_ids

    def get_channels(self, to_json=True):
        url = self.server + '/api/Inventory/GetChannels'
        response = self.request(url, to_json=to_json)
        channels = []
        for channel in response:
            channels.append(channel['Source'] + ' ' + channel['SubSource'])
        return channels

    def get_location_info(self, to_json=True):
        url = self.server + '/api/Inventory/GetStockLocations'
        response = self.request(url, to_json=to_json)
        locations = []
        for location in response:
            new_location = {}
            new_location['name'] = location['LocationName']
            new_location['id'] = location['StockLocationId']
            locations.append(new_location)
        return locations

    def get_location_ids(self):
        locations = []
        for location in self.get_location_info():
            locations.append(location['id'])
        return locations

    def get_location_names(self):
        locations = []
        for location in self.get_location_info():
            locations.append(location['name'])
        return locations

    def get_inventory_views(self, to_json=True):
        url = self.server + '/api/Inventory/GetInventoryViews'
        response = self.request(url, to_json=to_json)
        return response

    def get_new_inventory_view(self, to_json=True):
        url = self.server + '/api/Inventory/GetNewInventoryView'
        response = self.request(url, to_json=to_json)
        return response

    def get_inventory_column_types(self, to_json=True):
        url = self.server + '/api/Inventory/GetInventoryColumnTypes'
        response = self.request(url, to_json=to_json)
        return response

    def get_inventory_items(self, start=0, count=1, to_json=True):
        url = self.server + '/api/Inventory/GetInventoryItems'
        view = json.dumps(self.get_new_inventory_view())
        locations = json.dumps(self.get_location_ids())
        data = {'view' : view, 'stockLocationIds' : locations, 'startIndex' : start, 'itemsCount' : count}
        response = self.request(url, data, to_json=to_json)
        return response

    def get_inventory_list(self):
        item_count = self.get_inventory_items()['TotalItems']
        all_items = []
        for item in self.get_inventory_items(count=item_count)['Items']:
            all_items.append(InventoryItem(item))
        return all_items
        
    

api = LinnworksAPI()
