"""Creates new variation group """

import uuid

from pylinnworks.api_requests.request import Request
from pylinnworks.functions import get_new_SKU
from pylinnworks.functions import is_guid


class CreateVariationGroup(Request):
    url_extension = '/api/Stock/CreateVariationGroup'
    children_ids = []

    def __init__(self, api_session, sku=None, title=None, stock_id=None,
                 children_ids=None):
        if sku is not None:
            self.sku = sku
        else:
            self.sku = get_new_SKU()
        if title is not None:
            self.title = title
        if stock_id is not None:
            self.stock_id = stock_id
        else:
            self.stock_id = str(uuid.uuid4)
        if children_ids is not None:
            self.children_ids = children_ids
        super().__init__(api_session)

    def test_request(self):
        assert self.sku is not None and self.sku != '', \
            "SKU must be supplied."
        assert self.title is not None and self.title != '', \
            "Title must be supplied."
        assert is_guid(self.stock_id), \
            "Stock ID must be valid GUID."
        assert isinstance(self.children_ids, (list, set, tuple)), \
            "Children IDs must be in list or set."
        for child in self.children_ids:
            assert is_guid(child), "Children IDs must be valid GUID."
        return super().test_request

    def get_data(self):
        template = {}
        template['ParentSKU'] = self.sku
        template['VariationGroupName'] = self.title
        template['ParentStockItemId'] = self.stock_id
        template['VariationItemIds'] = self.children_ids
        data = {'template': json.dumps(template)}
        return data

    def test_response(self, response):
        assert response.text == '', "Error message recieved: " + response.text
        return super().test_response(response)
