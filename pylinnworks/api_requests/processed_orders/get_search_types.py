from pylinnworks.api_requests.request import Request


class GetSearchTypes(Request):
    url_extension = '/api/ProcessedOrders/GetSearchTypes'

    def process_response(self, response):
        self.order_json = self.json
        self.order_dict = self.response_dict
