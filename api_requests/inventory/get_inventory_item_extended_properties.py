"""Request extended properties for inventory item with stock ID stock_id """

from .. request import Request


class GetInventoryItemExtendedProperties(Request):
    url_extension = '/api/Inventory/GetInventoryItemExtendedProperties'

    def __init__(self, api_session, stock_id):
        self.stock_id = stock_id
        super().__init__(api_session)

    def get_data(self):
        data = {
            'inventoryItemId': self.stock_id
        }
        self.data = data
        return data
