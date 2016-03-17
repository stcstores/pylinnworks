from . update_inventory_item_field import UpdateInventoryItemField
from ... functions import is_guid
from ... info . get_categories import GetCategories


class UpdateCategory(UpdateInventoryItemField):
    field_name = 'Category'

    def __init__(self, api_session, value=None, stock_id=None):
        if value is not None:
            if is_guid(value):
                self.value = value
            else:
                self.value = GetCategories(api_session).id_lookup(value)
        if stock_id is not None:
            self.stock_id = stock_id
        super().__init__(api_session)
