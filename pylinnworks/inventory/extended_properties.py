import uuid

import pylinnworks.api_requests as api_requests
from . extended_property import ExtendedProperty


class ExtendedProperties():

    def __init__(self, item):
        self.item = item
        self.refresh()

    def refresh(self):
        self.extended_properties = []
        extended_property_data = api_requests.\
            GetInventoryItemExtendedProperties(
                self.item.stock_id).response_dict
        for property_data in extended_property_data:
            new_property = ExtendedProperty(
                property_id=property_data['pkRowId'],
                property_type=property_data['PropertyType'],
                name=property_data['ProperyName'],
                value=property_data['PropertyValue'],
                stock_id=self.item.stock_id)
            self.extended_properties.append(new_property)

    def __getitem__(self, key):
        if type(key) == int:
            return self.extended_properties[key]
        elif type(key) == str:
            for prop in self.extended_properties:
                if prop.name == key:
                    return prop

    def __iter__(self):
        for prop in self.extended_properties:
            yield prop

    def __len__(self):
        return len(self.extended_properties)

    def append(self, extended_property):
        self.extended_properties.append(extended_property)

    def create(self, name='', value='', property_type='Attribute'):
        extended_property = ExtendedProperty(
            property_id=str(uuid.uuid4()), property_type=property_type,
            name=name, value=value, stock_id=self.item.stock_id)
        api_requests.CreateInventoryItemExtendedProperties(
            [extended_property])
        self.refresh()
