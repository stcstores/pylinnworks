from . update_inventory_item_field import UpdateInventoryItemField


class UpdateInventoryItemTitle(UpdateInventoryItemField):
    field_name = 'Title'

    def __init__(self, api, value=None, stock_id=None):
        if value is not None:
            self.value = value
        if stock_id is not None:
            self.stock_id = stock_id
        super().__init__(api)
