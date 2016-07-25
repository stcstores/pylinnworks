from . update_inventory_item_field import UpdateInventoryItemField


class UpdateCategory(UpdateInventoryItemField):
    field_name = 'Category'

    def __init__(self, api_session, value=None, stock_id=None):
        if value is not None:
            self.value = value
        if stock_id is not None:
            self.stock_id = stock_id
        super().__init__(api_session)

    def test_request(self):
        assert is_guid(self.value), "Value must be valid GUID."
        return super().test_request(self)
