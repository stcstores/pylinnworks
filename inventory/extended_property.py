class ExtendedProperty():

    def __init__(self, item, json=None):
        self.item = item
        self.type = ''
        self.value = ''
        self.name = ''
        self.on_server = False
        self.delete = False
        if json is not None:
            self.load_from_json(json)
            self.on_server = True
        else:
            self.guid = str(uuid.uuid4())
            self.on_server = False

    def load_from_json(self, json):
        self.type = json['PropertyType']
        self.value = json['PropertyValue']
        self.name = json['ProperyName']
        self.guid = json['pkRowId']

    def get_json(self):
        data = {}
        data['pkRowId'] = self.guid
        data['fkStockItemId'] = self.item.stock_id
        data['ProperyName'] = self.name
        data['PropertyValue'] = self.value
        data['PropertyType'] = self.type
        return data

    def update(self):
        api_session = self.item.api_session
        url = api_session.server + ('/api/Inventory/'
                            'UpdateInventoryItemExtendedProperties')
        data = {
            'inventoryItemExtendedProperties': json.dumps([self.get_json()])}
        response = api_session.request(url, data)
        return response

    def create(self):
        api_session = self.item.api_session
        url = api_session.server + ('/api/Inventory/'
                            'CreateInventoryItemExtendedProperties')
        data = {
            'inventoryItemExtendedProperties': json.dumps([self.get_json()])}
        response = api_session.request(url, data)
        return response

    def remove(self):
        self.delete = True

    def delete_from_server(self):
        api_session = self.item.api_session
        data = {'inventoryItemId': self.item.stock_id,
                'inventoryItemExtendedPropertyIds': json.dumps([self.guid])}

        url = api_session.server + ('/api/Inventory/'
                            'DeleteInventoryItemExtendedProperties')
        response = api_session.request(url, data)
        return response
