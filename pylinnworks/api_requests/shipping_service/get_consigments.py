from pylinnworks.api_requests.request import Request


class GetConsigments(Request):
    url_extension = '/api/ShippingService/GetConsigments'

    def __init__(
            self, api_session, vendor, service_id, account_id, page_number=1,
            items_by_page=30):
        self.vendor = vendor
        self.service_id = service_id
        self.account_id = account_id
        self.page_number = page_number
        self.items_by_page = items_by_page
        super().__init__(api_session)

    def get_data(self):
        data = {
            'vendor': self.vendor,
            'serviceId': self.service_id,
            'pageNumber': self.page_number,
            'itemsByPage': self.items_by_page,
            'accountId': self.account_id
        }
        self.data = data
        return data

    def process_response(self, response):
        self.order_json = self.json
        self.order_dict = self.response_dict
