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

    def get_categories(self):
        url = api.server + '/api/Inventory/GetCategories'
        response = self.request(url)
        categories = []
        for category in response:
            categories.append(category['CategoryName'])
        return categories

    def get_channels(self):
        url = api.server + '/api/Inventory/GetChannels'
        response = self.request(url)
        channels = []
        for channel in response:
            channels.append(channel['Source'] + ' ' + channel['SubSource'])
        return channels
    

api = LinnworksAPI()
