"""LinkingList class.

Provides LinkingList class for containing ChannelItem instances.
Allows sorting for, and searching of channel items.
"""


class LinkingList:
    """Container for Linnworks selling channel items.

    Allows channel items to be sorted, filtered and searched.
    """

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
        """Get items from this list that are linked.

        Returns LinkingList.
        """
        return LinkingList([item for item in self.items if item.is_linked])

    def unlinked(self):
        """Get items from this list that are not linked.

        Returns LinkingList.
        """
        return LinkingList([item for item in self.items if not item.is_linked])

    def get_item_by_channel_sku(self, sku):
        """Return channel item mathching provided channel SKU.

        If no matching item is found raises ValueError.

        Args:
            sku
                type: str
                SKU of item to be found.

        Returns ChannelItem.
        """
        for item in self.items:
            if item.sku == sku:
                return item
        raise ValueError

    def get_item_by_linked_sku(self, sku):
        """Return channel item mathching provided inventory SKU.

        If no matching item is found raises ValueError.

        Args:
            sku
                type: str
                SKU of item to be found.

        Returns ChannelItem.
        """
        for item in self.items:
            if item.linked_sku == sku:
                return item
        raise ValueError
