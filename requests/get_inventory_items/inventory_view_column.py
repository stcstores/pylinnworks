import json


class InventoryViewColumn():
    column_name = ''
    display_name = ''
    field = 'String'
    group = 'General'
    is_editable = 'False'
    sort_direction = None
    width = 150.0

    def __init__(
            self, column_name=None, display_name=None, field=None, group=None,
            is_editable=None, sort_direction=None, width=None):
        self.column_name = column_name
        if column_name is not None:
            self.column_name = column_name
        if display_name is not None:
            self.display_name = display_name
        else:
            display_name = self.column_name
        if field is not None:
            self.field = field
        if group is not None:
            self.group = group
        if is_editable is not None:
            self.is_editable = is_editable
        if sort_direction is not None:
            self.sort_direction = sort_direction
        if width is not None:
            self.width = None

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
        column_dict['ColumnName'] = str(self.column_name)
        column_dict['DisplayName'] = str(self.display_name)
        column_dict['Field'] = str(self.field)
        column_dict['Group'] = str(self.group)
        column_dict['IsEditable'] = str(self.is_editable)
        column_dict['SortDirection'] = str(self.sort_direction)
        column_dict['Width'] = float(self.width)
        return column_dict

    def to_json(self):
        return json.dumps(self.to_dict())

    def load_from_json(self, column_json):
        self.load_from_dict(json.loads(column_json))
