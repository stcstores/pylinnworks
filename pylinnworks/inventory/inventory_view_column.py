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

    @classmethod
    def load_from_dict(cls, column_dict):
        cls.column_name = column_dict['ColumnName']
        cls.display_name = column_dict['DisplayName']
        cls.field = column_dict['Field']
        cls.group = column_dict['Group']
        cls.is_editable = column_dict['IsEditable']
        cls.sort_direction = column_dict['SortDirection']
        cls.width = column_dict['Width']

    @classmethod
    def to_dict(cls):
        column_dict = {}
        column_dict['ColumnName'] = cls.column_name
        column_dict['DisplayName'] = cls.display_name
        column_dict['Field'] = cls.field
        column_dict['Group'] = cls.group
        column_dict['IsEditable'] = cls.is_editable
        column_dict['SortDirection'] = str(cls.sort_direction)
        column_dict['Width'] = float(cls.width)
        return column_dict

    @classmethod
    def to_json(cls):
        return json.dumps(cls.to_dict())

    @classmethod
    def load_from_json(cls, column_json):
        cls.load_from_dict(json.loads(column_json))


class SKUColumn(InventoryViewColumn):
    column_name = 'SKU'
    display_name = 'SKU'
    group = 'General'
    field = 'String'
    sort_direction = 'None'
    width = 150
    is_editable = False


class TitleColumn(InventoryViewColumn):
    column_name = 'Title'
    display_name = 'Title'
    group = 'General'
    field = 'String'
    sort_direction = 'None'
    width = 250
    is_editable = True


class BarcodeColumn(InventoryViewColumn):
    column_name = 'Barcode'
    display_name = 'Barcode'
    group = 'General'
    field = 'String'
    sort_direction = 'None'
    width = 130
    is_editable = True


class RetailPriceColumn(InventoryViewColumn):
    column_name = 'RetailPrice'
    display_name = 'Retail'
    group = 'General'
    field = 'Double'
    sort_direction = 'None'
    width = 100
    is_editable = True


class PurchasePriceColumn(InventoryViewColumn):
    column_name = 'PurchasePrice'
    display_name = 'Purchase'
    group = 'General'
    field = 'Double'
    sort_direction = 'None'
    width = 75
    is_editable = True


class StockLevelColumn(InventoryViewColumn):
    column_name = 'StockLevel'
    display_name = 'Level'
    group = 'Stock'
    field = 'Int'
    sort_direction = 'None'
    width = 75
    is_editable = False


class InOrderColumn(InventoryViewColumn):
    column_name = 'InOrder'
    display_name = 'In+Open+Orders'
    group = 'Stock'
    field = 'Int'
    sort_direction = 'None'
    width = 75
    is_editable = False


class AvailableColumn(InventoryViewColumn):
    column_name = 'Available'
    display_name = 'Available'
    group = 'Stock'
    field = 'Int'
    sort_direction = 'None'
    width = 75
    is_editable = False


class MinimumLevelColumn(InventoryViewColumn):
    column_name = 'MinimumLevel'
    display_name = 'Minimum+Level'
    group = 'Stock'
    field = 'Int'
    sort_direction = 'None'
    width = 75
    is_editable = True


class TrackedColumn(InventoryViewColumn):
    column_name = 'Tracked'
    display_name = 'Tracked'
    group = 'General'
    field = 'Boolean'
    sort_direction = 'None'
    width = 75
    is_editable = False


class CreatedDateColumn(InventoryViewColumn):
    column_name = 'CreatedDate'
    display_name = 'CreatedDate'
    group = 'General'
    field = 'Date'
    sort_direction = 'None'
    width = 108
    is_editable = False


class DueColumn(InventoryViewColumn):
    column_name = 'Due'
    display_name = 'Due'
    group = 'Stock'
    field = 'Int'
    sort_direction = 'None'
    width = 75
    is_editable = False


class ImageColumn(InventoryViewColumn):
    column_name = 'Image'
    display_name = 'Image'
    group = 'General'
    field = 'Boolean'
    sort_direction = 'None'
    width = 80
    is_editable = False


class ModifiedDateColumn(InventoryViewColumn):
    column_name = 'ModifiedDate'
    display_name = 'Modified+Date'
    group = 'General'
    field = 'Date'
    sort_direction = 'None'
    width = 108
    is_editable = False


class StockValueColumn(InventoryViewColumn):
    column_name = 'StockValue'
    display_name = 'Stock+Value'
    group = 'Stock'
    field = 'Double'
    sort_direction = 'None'
    width = 75
    is_editable = True


class VariationGroupNameColumn(InventoryViewColumn):
    column_name = 'VariationGroupName'
    display_name = 'Variation+Group+Name'
    group = 'General'
    field = 'String'
    sort_direction = 'None'
    width = 160
    is_editable = True


class CategoryColumn(InventoryViewColumn):
    column_name = 'Category'
    display_name = 'Category'
    group = 'General'
    field = 'Select'
    sort_direction = 'None'
    width = 75
    is_editable = True


class BinRackColumn(InventoryViewColumn):
    column_name = 'BinRack'
    display_name = 'BinRack'
    group = 'Location'
    field = 'String'
    sort_direction = 'None'
    width = 75
    is_editable = True

ALL_COLUMNS = [
    SKUColumn,
    TitleColumn,
    BarcodeColumn,
    RetailPriceColumn,
    PurchasePriceColumn,
    StockLevelColumn,
    InOrderColumn,
    AvailableColumn,
    MinimumLevelColumn,
    TrackedColumn,
    CreatedDateColumn,
    DueColumn,
    ImageColumn,
    ModifiedDateColumn,
    StockValueColumn,
    VariationGroupNameColumn,
    CategoryColumn,
    BinRackColumn,
]
