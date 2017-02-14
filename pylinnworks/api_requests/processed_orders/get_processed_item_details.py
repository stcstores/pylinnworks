from pylinnworks import PyLinnworks
from pylinnworks.api_requests.request import Request


class GetProcessedItemDetails(Request):
    url_extension = '/api/ProcessedOrders/GetProcessedItemDetails'

    def __init__(
            self, order_id, include_children=True,
            include_item_options=False):
        self.order_id = order_id
        self.include_children = include_children
        self.include_item_options = include_item_options
        super().__init__(PyLinnworks)

    def get_data(self):
        data = {
            'includeChildren': self.include_children,
            'includeItemOptions': self.include_item_options,
            'pkOrderId': self.order_id}
        self.data = data
        return data
