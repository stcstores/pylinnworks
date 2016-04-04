class ExtendedProperties():

    def __init__(self, item, load=True):
        self.item = item
        self.extended_properties = []
        if load is True:
            self.load()

    def __getitem__(self, key):
        if type(key) == int:
            return self.extended_properties[key]
        elif type(key) == str:
            for prop in self.extended_properties:
                if prop.name == key:
                    return prop

    def __iter__(self):
        for prop in self.extended_properties:
            yield prop

    def __len__(self):
        return len(self.extended_properties)

    def append(self, extended_property):
        self.extended_properties.append(extended_property)

    def load(self):
        response = self.api_session.get_inventory_item_extended_properties(
            self.item.stock_id)
        for _property in response:
            self.add(json=_property)

    def add(self, json):
        self.extended_properties.append(
            _ExtendedProperty(self.item, json=json))

    def create(self, name='', value='', property_type='Attribute'):
        prop = ExtendedProperty(self.item)
        prop.name = name
        prop.value = value
        prop.type = property_type
        self.extended_properties.append(prop)
        return prop

    def create_on_server(self, name='', value='', property_type='Attribute'):
        prop = self.create(name=name, value=value, property_type=property_type)
        prop.create()

    def upload_new(self):
        new_properties = []
        for prop in self.extended_properties:
            if prop.on_server is False:
                new_properties.append(prop)
        if len(new_properties) > 0:
            item_arrays = []
            for prop in new_properties:
                item_arrays.append(prop.get_json())
            data = {
                'inventoryItemExtendedProperties': json.dumps(item_arrays)}
            api_session = self.item.api_session
            url = api_session.server + ('/api/Inventory/'
                                'CreateInventoryItemExtendedProperties')
            response = api_session.request(url, data)
            return response

    def update_existing(self):
        new_properties = []
        for prop in self.extended_properties:
            if prop.on_server is True:
                new_properties.append(prop)
        if len(new_properties) > 0:
            item_arrays = []
            for prop in new_properties:
                item_arrays.append(prop.get_json())
            data = {
                'inventoryItemExtendedProperties': json.dumps(item_arrays)}
            api_session = self.item.api_session
            url = api_session.server + ('/api/Inventory/'
                                'UpdateInventoryItemExtendedProperties')
            response = api_session.request(url, data)
            return response

    def remove_deleted(self):
        api_session = self.item.api_session
        items_to_delete = []
        for prop in self:
            if prop.delete is True:
                items_to_delete.append(prop.guid)
        if len(items_to_delete) > 0:
            data = {
                'inventoryItemId': self.item.stock_id,
                'inventoryItemExtendedPropertyIds': json.dumps(
                    items_to_delete)}
            url = api_session.server + ('/api/Inventory/'
                                'DeleteInventoryItemExtendedProperties')
            response = api_session.request(url, data)
            return response

    def update(self):
        self.upload_new()
        self.update_existing()
        self.remove_deleted()
