from pylinnworks.api_requests.request import Request


class GetManifests(Request):
    url_extension = '/api/ShippingService/GetManifests'

    def __init__(self, api_session):
        super().__init__(api_session)

    def process_response(self, response):
        self.order_json = self.json
        self.order_dict = self.response_dict
