from . update_inventory_item_stock_field import UpdateInventoryItemStockField


class UpdateAvailable(UpdateInventoryItemStockField):
    field_name = 'Barcode'

    def __init__(self, api_session, value=None, stock_id=None,
                 location_id=None):
        if value is not None:
            self.value = value
        if stock_id is not None:
            self.stock_id = stock_id
        if location_id is not None:
            self.location_id = location_id
        super().__init__(api_session)
