"""Requests open order IDs """

from .. request import Request
from .. info . get_locations import GetLocations


class GetOpenOrderIDs(Request):
    url_extension = '/api/Orders/GetAllOpenOrders'
    filters = {}
    location_id = ''
    additional_filter = ''

    def __init__(self, api, filters=None, location_id=None,
                 additional_filter=None):
        if filters is not None:
            self.filters = filters
        if location_id is not None:
            self.location_id = location_id
        else:
            self.location_id = GetLocations.default
        super().__init__(api)

    def get_data(self):
        data = {
            'filters': self.filters,
            'fulfilmentCenter': self.location_id,
            'additionalFilter': self.additional_filter
        }
        self.data = data
        return data
