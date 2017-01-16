import json


class InventoryViewColumn():

    def __init__(
            self, column_name='', display_name='', field='String',
            group='General', is_editable=False, sort_direction=None,
            width=150.0):
        self.column_name = column_name
        self.display_name = display_name
        self.field = field
        self.group = group
        self.is_editable = is_editable
        self.sort_direction = sort_direction
        self.width = width

    def load_from_dict(self, column_dict):
        self.column_name = column_dict['ColumnName']
        self.display_name = column_dict['DisplayName']
        self.field = column_dict['Field']
        self.group = column_dict['Group']
        self.is_editable = column_dict['IsEditable']
        self.sort_direction = column_dict['SortDirection']
        self.width = column_dict['Width']

    def to_dict(self):
        column_dict = {}
        column_dict['ColumnName'] = self.column_name
        column_dict['DisplayName'] = self.display_name
        column_dict['Field'] = self.field
        column_dict['Group'] = self.group
        column_dict['IsEditable'] = self.is_editable
        column_dict['SortDirection'] = str(self.sort_direction)
        column_dict['Width'] = float(self.width)
        return column_dict

    def to_json(self):
        return json.dumps(self.to_dict())

    def load_from_json(self, column_json):
        self.load_from_dict(json.loads(column_json))
