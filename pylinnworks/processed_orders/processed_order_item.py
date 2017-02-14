"""ProcessedOrderItem class."""


class ProcessedOrderItem:
    """Container for processed order item."""

    def __init__(self, item_data):
        """Load data from GetProcessedItemDetails request."""
        self.order_item_id = item_data['OrderItemRowId']
        self.quantity = item_data['Quantity']
        self.stock_id = item_data['pkStockItemId']
        self.sku = item_data['SKU']
        self.title = item_data['ItemTitle']
        self.despatch_unit_cost = item_data['DespatchUnitCost']
        self.cost_ex_tax = item_data['CostExTax']
        self.cost_inc_tax = item_data['CostIncTax']
        self.per_unit_inc_tax = item_data['PerUnitIncTax']
        self.per_unit_ex_tax = item_data['PerUnitExTax']
        self.tax_rate = item_data['TaxRate']
        self.total_tax = item_data['TotalTax']
        self.line_discount = item_data['LineDiscount']
        self.tax_cost_inclusive = item_data['TaxCostInclusive']
        self.note = item_data['Note']
        self.parent_item_id = item_data['ParentItemRowId']
        self.has_children = item_data['HasChildren']
        self.child_items = item_data['ChildItems']
        self.has_options = item_data['HasOptions']
        self.options = item_data['Options']

    def __repr__(self):
        return '{}X {} - {}'.format(self.quantity, self.sku, self.title)
