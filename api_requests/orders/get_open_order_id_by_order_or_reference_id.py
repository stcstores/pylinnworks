"""Requests order_id for order_number """

import json

from .. request import Request


class GetOpenOrderIDByOrderOrReferenceID(Request):
    url_extension = '/api/Orders/GetOpenOrderIdByOrderOrReferenceId'
    filters = {}
    order_number = ''

    def __init__(self, api_session, order_number=None, filters=None):
        if order_number is not None:
            self.order_number = order_number
        if filters is not None:
            self.filters = filters
        super().__init__(api_session)

    def get_data(self):
        data = {
            'orderOrReferenceId': self.order_number,
            'filters': json.dumps(self.filters)
        }
        self.data = data
        return data

    def process_response(self, response):
        self.order_id = self.response_dict
