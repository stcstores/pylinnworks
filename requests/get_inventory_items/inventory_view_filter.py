import json


class InventoryViewFilter():
    field = ''
    value = ''
    filter_name = ''
    filter_name_exact = ''
    condition = ''

    def __init__(self, field=None, value=None, condition=None, filter_name=None,
                 filter_name_exact=None):
        if field is not None:
            self.field = field
        if value is not None:
            self.value = value
        if condition is not None:
            self.condition = condition
        if filter_name is not None:
            self.filter_name = filter_name
        if filter_name_exact is not None:
            self.filter_name_exact = filter_name_exact

    def to_dict(self):
        filter_dict = {}
        filter_dict['Value'] = self.value
        filter_dict['Field'] = self.field
        filter_dict['FilterName'] = self.fitler_name
        filter_dict['FilterNameExact'] = self.filter_name_exact
        filter_dict['Condition'] = self.condition
        return filter_dict

    def load_from_dict(self, filter_dict):
        self.value = filter_dict['Value']
        self.field = filter_dict['Field']
        self.filter_name = filter_dict['FilterName']
        self.filter_name_exact = filter_dict['FilterNameExact']
        self.condition = filter_dict['Condition']

    def to_json(self):
        return json.dumps(self.to_dict())

    def load_from_json(self, filter_json):
        self.load_from_dict(json.loads(filter_json))
