from . update_inventory_item_field import UpdateInventoryItemField


class UpdatePurchasePrice(UpdateInventoryItemField):
    field_name = 'PurchasePrice'

    def __init__(self, api_session, value=None, stock_id=None):
        if value is not None:
            self.value = value
        if stock_id is not None:
            self.stock_id = stock_id
        super().__init__(api_session)

    def test_request(self):
        assert isinstance(self.value, float), "Value must be of type float"
        return super().test_request(self)
