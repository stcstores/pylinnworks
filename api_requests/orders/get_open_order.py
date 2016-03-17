"""Gets order data for order with order ID order_id """

from .. request import Request
from .. info . get_locations import GetLocations
from ... open_order import OpenOrder


class GetOpenOrder(Request):
    url_extension = '/api/Orders/GetOrder'
    load_items = True
    load_additional_info = False

    def __init__(self, api_session, order_id, location_id=None,
                 load_items=None, load_additional_info=None):
        self.order_id = order_id
        if location_id is not None:
            self.location_id = location_id
        else:
            location_id = GetLocations.default
        if location_id is not None:
            self.location_id = location_id
        if load_items is not None:
            self.load_items = load_items
        if load_additional_info is not None:
            self.load_additional_info = load_additional_info
        super().__init__(api_session)

    def get_data(self):
        data = {
            'orderId': self.order_id,
            'fulfilmentLocationId': self.location_id,
            'loadItems': self.load_items,
            'loadAdditionalInfo': self.load_additional_info
        }
        self.data = data
        return data

    def process_response(self, response):
        self.order_json = self.json
        self.order_dict = self.response_dict
        self.order = OpenOrder(self.response_dict)
