import json


class InventoryViewFilter:

    def __init__(
            self, filter_name='General', field='String', value=None,
            condition='contains', filter_logic='AND', filter_name_exact=None,
            condition_display_name='Contains', display_name='Anything'):
        self.filter_name = filter_name
        self.field = field
        self.value = value
        self.condition = condition
        self.filter_logic = filter_logic
        self.filter_name_exact = filter_name_exact
        self.condition_display_name = condition_display_name
        self.display_name = display_name

    def to_dict(self):
        filter_dict = {
            "FilterName": self.filter_name,
            "DisplayName": self.display_name,
            "FilterNameExact": None,
            "Field": self.field,
            "Condition": self.condition,
            "ConditionDisplayName": self.condition_display_name,
            "FilterLogic": self.filter_logic,
            "Value": self.value,
            }
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
