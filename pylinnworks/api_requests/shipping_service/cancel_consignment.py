from pylinnworks.api_requests import Request


class CancelConsignment(Request):
    url_extension = '/api/ShippingService/CancelConsignment'

    def __init__(
            self, api_session, vendor, account_id, consignment_id, order_id):
        self.vendor = vendor
        self.account_id = account_id
        self.consignment_id = consignment_id
        self.order_id = order_id
        super().__init__(api_session)

    def get_data(self):
        data = {
            'vendor': self.vendor,
            'accountId': self.account_id,
            'consignmentId': self.consignment_id,
            'orderId': self.order_id}
        self.data = data
        return data

    def process_response(self, response):
        self.order_json = self.json
        self.order_dict = self.response_dict
