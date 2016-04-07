import linnapi.api_requests


class ExtendedProperty():

    def __init__(
            self, property_type=None, value=None, name=None, property_id=None,
            item_stock_id=None):
        self.property_type = None
        self.value = None
        self.name = None
        self.property_id = None
        if property_type is not None:
            self.property_type = property_type
        if value is not None:
            self.value = value
        if name is not None:
            self.name = name
        if property_id  is not None:
            self.property_id = property_id
        if item_stock_id is not None:
            self.item_stock_id = item_stock_id

    def get_extended_properties_dict(self):
        ex_prop = {
            'pkRowId': self.property_id,
            'ProperyName': self.name,
            'PropertyValue': self.value,
            'PropertyType': self.property_type
        }
        return ex_prop

    def update(self):
        extended_properties = [self.get_extended_properties_dict()]
        request = linnapi.api_requests.UpdateInventoryItemExtendedProperties(
            self.api_session, extended_properties)

    def create(self):
        extended_properties = [self.get_extended_properties_dict()]
        request = CreateInventoryItemExtendedProperties(
            self.api_session, extended_properties)

    def delete_from_server(self):
        api_session = self.item.api_session
        data = {'inventoryItemId': self.item.stock_id,
                'inventoryItemExtendedPropertyIds': json.dumps([self.guid])}

        url = api_session.server + ('/api/Inventory/'
                            'DeleteInventoryItemExtendedProperties')
        response = api_session.request(url, data)
        return response
