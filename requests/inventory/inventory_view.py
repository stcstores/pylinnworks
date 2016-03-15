import json
import uuid

from . inventory_view_column import InventoryViewColumn
from . inventory_view_filter import InventoryViewFilter


class InventoryView():
    channels = []
    columns = []
    country_code = None
    filters = []
    _id = None
    include_products = 'ALL'
    listing = 'ALL'
    mode = 'ALL'
    name = None
    show_only_changed = False
    source = None
    sub_source = None

    def __init__(self, name=None, _id=None):
        if _id is None:
            self._id = str(uuid.uuid4())
        else:
            self._id = _id

    def load_from_dict(self, view_dict):
        self.channels = view_dict['Channels']
        self.columns = []
        for column in view_dict['Columns']:
            new_column = InventoryViewColumn()
            new_column.load_from_dict(column)
            self.columns.append(new_column)
        self.country_code = view_dict['CountryCode']
        self.filters = []
        for view_filter in view_dict['Filters']:
            new_filter = InventoryViewFilter()
            new_filter.load_from_dict(view_filter)
            self.filters.append(new_filter)
        self._id = view_dict['Id']
        self.include_products = view_dict['IncludeProducts']
        self.listing = view_dict['Listing']
        self.mode = view_dict['Mode']
        self.name = view_dict['Name']
        self.show_only_changed = view_dict['ShowOnlyChanged']
        self.source = view_dict['Source']
        self.sub_source = view_dict['SubSource']

    def get_columns_list(self):
        column_list = []
        for column in self.columns:
            column_list.append(column.to_dict())
        return column_list

    def get_filters_list(self):
        filter_list = []
        for _filter in self.filters:
            filter_list.append(_filter.to_dict())
        return filter_list

    def to_dict(self):
        view_dict = {}
        view_dict['Channels'] = self.channels
        view_dict['Columns'] = self.get_columns_list()
        view_dict['CountryCode'] = str(self.country_code)
        view_dict['Filters'] = self.get_filters_list()
        view_dict['Id'] = self._id
        view_dict['IncludeProducts'] = str(self.include_products)
        view_dict['Listing'] = str(self.listing)
        view_dict['Mode'] = str(self.mode)
        view_dict['Name'] = str(self.name)
        view_dict['ShowOnlyChanged'] = self.show_only_changed
        view_dict['Source'] = str(self.source)
        view_dict['SubSource'] = str(self.sub_source)
        return view_dict

    def to_json(self):
        return json.dumps(self.to_dict())

    def load_from_json(self, view_json):
        return self.load_from_dict(json.loads(view_json))
