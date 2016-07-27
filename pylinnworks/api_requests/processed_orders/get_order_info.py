"""Gets order data for order with order ID order_id """

from pylinnworks.api_requests.request import Request


class GetOrderInfo(Request):
    url_extension = '/api/ProcessedOrders/GetOrderInfo'

    def __init__(self, api_session, order_id):
        self.order_id = order_id
        super().__init__(api_session)

    def get_data(self):
        data = {
            'pkOrderId': self.order_id,
        }
        self.data = data
        return data

    def process_response(self, response):
        self.order_json = self.json
        self.order_dict = self.response_dict
