"""Gets data for list of order IDs """

import json

from linnapi.api_requests.request import Request


class GetOrders(Request):
    url_extension = '/api/Orders/GetOrders'
    order_ids = []
    location_id = ''
    load_items = True
    load_additional_info = True

    def __init__(self, api_session, order_ids=None, location_id=None,
                 load_items=None, load_additional_info=None):
        if order_ids is not None:
            self.order_ids = order_ids
        if location_id is not None:
            self.location_id = location_id
        else:
            self.location_id = self.api_session.locations['Default'].guid
        if load_items is not None:
            self.load_items = load_items
        if load_additional_info is not None:
            self.load_additional_info = load_additional_info
        super().__init__(api_session)

    def get_data(self):
        data = {
            'ordersIds': json.dumps(self.order_ids),
            'fulfilmentLocationId': self.location_id,
            'loadItems': self.load_items,
            'loadAdditionalInfo': self.load_additional_info
        }
        self.data = data
        return data
