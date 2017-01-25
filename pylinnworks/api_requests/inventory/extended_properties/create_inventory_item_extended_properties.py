import json

from pylinnworks import PyLinnworks
from pylinnworks.api_requests.request import Request


class CreateInventoryItemExtendedProperties(Request):

    url_extension = '/api/Inventory/CreateInventoryItemExtendedProperties'

    def __init__(self, extended_properties):
        self.extended_properties = extended_properties
        super().__init__(PyLinnworks)

    def get_data(self):
        self.data = {
            'inventoryItemExtendedProperties': json.dumps([{
                    "pkRowId": prop.property_id,
                    "fkStockItemId": prop.stock_id,
                    "ProperyName": prop.name,
                    "PropertyValue": prop.value,
                    "PropertyType": prop.property_type
                } for prop in self.extended_properties])
            }
        return self.data
