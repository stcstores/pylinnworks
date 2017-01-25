from pylinnworks import PyLinnworks
from pylinnworks.api_requests.request import Request


class UpdateInventoryItemExtendedProperties(Request):
    url_extension = '/api/Inventory/UpdateInventoryItemExtendedProperties'

    def __init__(
            self, extended_property_id, name='', value='', property_type=''):
        self.extended_property_id = extended_property_id
        self.name = name
        self.value = value
        self.property_type = property_type
        super().__init__(PyLinnworks)

    def get_data(self):
        data = {
            'pkRowId': self.extended_property_id,
            'ProperyName': self.name,
            'PropertyValue': self.value,
            'PropertyType': self.property_type
        }
        self.data = data
        return data
