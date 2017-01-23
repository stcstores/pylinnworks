"""InventoryList class.

Container for multiple InventoryItem objects.
"""


class InventoryList:
    """Container for multiple InventoryItem objects.

    Allows lists of inventory items to be sorted and searched.
    """

    def __init__(self, api_session, items=[]):
        self.api_session = api_session
        self.items = items

    def __getitem__(self, key):
        return self.items[key]

    def __iter__(self):
        for item in self.items:
            yield item

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        return 'Inventory list containing {} items'.format(len(self))

    def append(self, item):
        """Add item to list."""
        self.items.append(item)

    def sku(self, sku):
        """Get item from list by SKU."""
        items = [item for item in self.items if item.sku == sku]
        if len(items) == 1:
            return items[0]
        elif len(items) > 1:
            raise IndexError('SKU not found')
        else:
            raise IndexError('Multiple items found')

    def title(self, title):
        """Get item from list by title."""
        items = [item for item in self.items if item.title == title]
        if len(items) == 1:
            return items[0]
        elif len(items) > 1:
            raise IndexError('Title not found')
        else:
            raise IndexError('Multiple items found')

    def stock_id(self, stock_id):
        """Get item from list by stock_id."""
        items = [item for item in self.items if item.stock_id == stock_id]
        if len(items) == 1:
            return items[0]
        elif len(items) > 1:
            raise IndexError('Stock ID not found')
        else:
            raise IndexError('Multiple items found')
