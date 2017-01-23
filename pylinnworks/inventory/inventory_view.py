import json
import uuid

from . inventory_view_column import InventoryViewColumn
from . inventory_view_column import InventoryViewColumns
from . inventory_view_filter import InventoryViewFilter
from .. pylinnworks import PyLinnworks


class InventoryView():

    def __init__(
            self, channels=[], columns=None, filters=[], country_code=None,
            name=None, id_=None, include_products='NotArchived', listing='ALL',
            mode='ALL', show_only_changed=False, source='All',
            sub_source='Show all', include_archived=False):
        self.channels = channels
        self.country_code = country_code
        self.filters = filters
        self.id_ = id_
        self.include_products = include_products
        self.listing = listing
        self.mode = mode
        self.name = name
        self.show_only_changed = show_only_changed
        self.source = source
        self.sub_source = sub_source
        self.include_archived = include_archived
        if self.id_ is None:
            self.id_ = str(uuid.uuid4())
        if columns is None:
            self.columns = InventoryViewColumns(PyLinnworks).columns
        else:
            self.columns = columns

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
        self.id_ = view_dict['Id']
        self.include_products = view_dict['IncludeProducts']
        self.listing = view_dict['Listing']
        self.mode = view_dict['Mode']
        self.name = view_dict['Name']
        self.show_only_changed = view_dict['ShowOnlyChanged']
        self.source = view_dict['Source']
        self.sub_source = view_dict['SubSource']

    def get_columns_list(self):
        return [col.to_dict() for col in self.columns]

    def get_filters_list(self):
        return [fil.to_dict() for fil in self.filters]

    def to_dict(self):
        view_dict = {
            'Channels': self.channels,
            'Columns': self.get_columns_list(),
            'CountryCode': self.country_code,
            'CountryName': None,
            'Filters': self.get_filters_list(),
            'Id': self.id_,
            'IncludeProducts': 'ALL',
            'Listing': self.listing,
            'Mode': self.mode,
            'Name': self.name,
            'ShowOnlyChanged': self.show_only_changed,
            'Source': self.source,
            'SubSource': self.sub_source,
            # "IsPredefined": True,
            "IsSearchRequired": True}
        return view_dict

    def to_json(self):
        return json.dumps(self.to_dict())

    def load_from_json(self, view_json):
        return self.load_from_dict(json.loads(view_json))
