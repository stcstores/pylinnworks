"""Requests open order IDs """

import json

from pylinnworks.api_requests.request import Request


class GetOpenOrders(Request):
    url_extension = '/api/Orders/GetOpenOrders'
    url_server = 'https://eu1.linnworks.net'
    filters = {}
    location_id = ''
    additional_filter = ''
    count = 99999
    page_number = 1

    def __init__(self, api_session, count=None, page_number=None, filters=None,
                 location_id=None, additional_filter=None):
        if count is not None:
            self.count = count
        if page_number is not None:
            self.page_number = page_number
        if filters is not None:
            self.filters = filters
        if location_id is not None:
            self.location_id = location_id
        else:
            self.location_id = self.api_session.locations['Default'].guid
        super().__init__(api_session)

    def get_data(self):
        data = {
            'filters': '',
            'fulfilmentCenter': self.location_id,
            'additionalFilter': '',
            'entriesPerPage': self.count,
            'sorting': [],
            'pageNumber': self.page_number
        }
        self.data = data
        return data
