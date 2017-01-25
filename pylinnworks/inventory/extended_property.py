import pylinnworks.api_requests as api_requests


class ExtendedProperty():

    def __init__(
            self, property_id=None, property_type='', name='',
            value='', stock_id=None):
        self.property_id = property_id
        self.property_type = property_type
        self.name = name
        self.value = value
        self.stock_id = stock_id

    def update(self):
        api_requests.UpdateInventoryItemExtendedProperties(
            extended_property_id=self.property_id, name=self.name,
            value=self.value, property_type=self.property_type)

    def delete(self):
        api_requests.DeleteInventoryItemExtendedProperties(
            stock_id=self.stock_id, property_ids=[self.property_id])
