class LinkingList:
    def __init__(self, items):
        self.items = items

    def __getitem__(self, index):
        return self.items[index]

    def __len__(self):
        return len(self.items)

    def __add__(self, other):
        items = self.items + other.items
        return LinkingList(items)

    def __repr__(self):
        return 'LinkingList containing {} items'.format(len(self.items))

    def linked(self):
        return LinkingList([item for item in self.items if item.is_linked])

    def unlinked(self):
        return LinkingList([item for item in self.items if not item.is_linked])

    def get_item_by_channel_sku(self, sku):
        for item in self.items:
            if item.sku == sku:
                return item
        raise ValueError

    def get_item_by_linked_sku(self, sku):
        for item in self.items:
            if item.linked_sku == sku:
                return item
        raise ValueError
