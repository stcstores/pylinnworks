import urllib.request
import requests
import json
from pprint import pprint

class LinnworksAPI:
    def __init__(self):
        self.username = 'stcstores@yahoo.com'
        self.password = input('Linnworks Password: ')
        self.get_token()
        

    def get_page(self, url, data=None):
        if data != None:
            data = urllib.parse.urlencode(data)
            data = data.encode('utf-8')
        with urllib.request.urlopen(url, data, timeout=120) as response:
            page = str(response.read())
            return page

    def make_request(self, url, data=None):
        request = requests.get(url, params=data)
        #print(request.url)
        parsed_json = json.loads(request.text)
        #pprint(parsed_json)
        return parsed_json

    def request(self, url, data=None):
        if data == None:
            data = {}
        data['token'] = self.token
        return self.make_request(url, data)

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

    def get_category_info(self):
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
        category_names = []
        for category in self.get_category_info():
            category_names.append(category['name'])
        return category_names

    def get_category_ids(self):
        category_ids = []
        for category in self.get_category_info():
            category_ids.append(category['id'])
        return category_ids

    def get_channels(self):
        url = self.server + '/api/Inventory/GetChannels'
        response = self.request(url)
        channels = []
        for channel in response:
            channels.append(channel['Source'] + ' ' + channel['SubSource'])
        return channels

    def get_stock_location_ids(self):
        url = self.server + '/api/Inventory/GetStockLocations'
        response = self.request(url)
        stock_location_ids = []
        for location in response:
            stock_location_ids.append(location['StockLocationId'])
        return stock_location_ids
    

api = LinnworksAPI()
