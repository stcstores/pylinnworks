"""Requests open order IDs """

from linnapi.api_requests.request import Request


class GetAllOpenOrders(Request):
    url_extension = '/api/Orders/GetAllOpenOrders'
    filters = {}
    location_id = ''
    additional_filter = ''

    def __init__(self, api_session, filters=None, location_id=None,
                 additional_filter=None):
        if filters is not None:
            self.filters = filters
        if location_id is not None:
            self.location_id = location_id
        else:
            self.location_id = self.api_session.locations['Default'].guid
        super().__init__(api_session)

    def get_data(self):
        data = {
            'filters': self.filters,
            'fulfilmentCenter': self.location_id,
            'additionalFilter': self.additional_filter
        }
        self.data = data
        return data
