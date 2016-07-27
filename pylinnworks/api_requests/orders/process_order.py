"""Processes order with order ID order_id """

from pylinnworks.api_requests.request import Request


class ProcessOrder(Request):
    url_extension = '/api/Orders/ProcessOrder'
    scan_performed = True

    def __init__(self, api_session, order_id, scan_performed=None):
        self.order_id = order_id
        if scan_performed is not None:
            self.scan_performed = scan_performed
        super().__init__(api_session)

    def get_data(self):
        data = {
            'orderId': self.order_id,
            'scanPerformed': self.scan_performed
        }
        self.data = data
        return data
