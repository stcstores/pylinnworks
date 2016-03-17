"""Creates new variation group """

import uuid

from .. request import Request
from .. functions import get_new_SKU


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

    def get_data(self):
        template = {}
        template['ParentSKU'] = self.sku
        template['VariationGroupName'] = self.title
        template['ParentStockItemId'] = self.stock_id
        template['VariationItemIds'] = self.children_ids
        data = {'template': json.dumps(template)}
        self.data = data
        return data
