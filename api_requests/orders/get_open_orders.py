"""Requests open order IDs """

from .. request import Request
from .. info . get_locations import GetLocations


class GetOpenOrders(Request):
    url_extension = '/api/Orders/GetOpenOrders'
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
            self.location_id = GetLocations.default
        super().__init__(api_session)

    def get_data(self):
        data = {
            'filters': self.filters,
            'fulfilmentCenter': self.location_id,
            'additionalFilter': self.additional_filter,
            'entriesPerPage': self.count,
            'pageNumber': self.page_number
        }
        self.data = data
        return data
