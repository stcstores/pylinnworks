"""Updates stock fields for inventory items """

from linnapi.api_requests.request import Request
from linnapi.api_requests.settings.get_locations import GetLocations


class UpdateInventoryItemStockField(Request):
    url_extension = '/api/Inventory/UpdateInventoryItemField'
    field_name = ''
    field_value = ''
    inventory_item_id = ''
    location_id = ''

    def __init__(self, api_session, field_name=None, value=None, stock_id=None,
                 location_id=None):
        if field_name is not None:
            self.field_name = field_name
        if value is not None:
            self.value = value
        if stock_id is not None:
            self.stock_id = stock_id
        if location_id is None:
            self.location_id = GetLocations.default
        super().__init__(api_session)

    def test_response(self, response):
        assert reponse.text == '', "Error message recieved: " + response.text
        return super().test_response(response)

    def get_data(self):
        data = {
            'fieldName': self.field_name,
            'fieldValue': self.value,
            'inventoryItemId': self.stock_id,
            'locationId': self.location_id
        }
        return data

    def test_request(self):
        assert self.field_name is not None and len(self.field_name) > 0, \
            "Field name must be supplied."
        assert self.value is not None and value != '', \
            "Value must be supplied."
        assert is_guid(self.stock_id), "Stock ID must be a valid GUID."
        assert is_guid(self.location_id), "Location ID must be a valid GUID."
        return super().test_request(request)
