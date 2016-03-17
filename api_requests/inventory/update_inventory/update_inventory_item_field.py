"""Updates fields for inventory items """

from ... request import Request


class UpdateInventoryItemField(Request):
    url_extension = '/api/Inventory/UpdateInventoryItemField'
    field_name = ''
    field_value = ''
    inventory_item_id = ''

    def __init__(self, api_session, field_name=None, value=None, stock_id=None):
        if field_name is not None:
            self.field_name = field_name
        if value is not None:
            self.value = value
        if stock_id is not None:
            self.stock_id = stock_id
        super().__init__(api_session)

    def get_data(self):
        data = {
            'fieldName': self.field_name,
            'fieldValue': self.value,
            'inventoryItemId': self.stock_id
        }
        self.data = data
        return data
