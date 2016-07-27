class InventoryItems:

    def __init__(self):
        self.items = []
        self.skus = []
        self.stock_ids = []
        self.titles = []

        self.sku_lookup = {}
        self.stock_id_lookup = {}
        self.title_lookup = {}

    def __getitem__(self, key):
        if key in self.stock_id_lookup:
            return self.items[self.stock_id_lookup[key]]
        if key in self.sku_lookup:
            return self.items[self.sku_lookup[key]]
        if key in self.title_lookup:
            return self.items[self.title_lookup[key]]
        if isinstance(key, int) and key >= 0 and key < len(self.items):
            return self.items[key]
        raise KeyError(key + " not in inventory items")

    def __iter__(self):
        for item in self.items:
            yield item

    def __len__(self):
        return len(self.items)

    def index(self, item):
        return self.items.index(item)

    def append(self, item):
        self.items.append(item)
        self.skus.append(item.sku)
        self.stock_ids.append(item.stock_id)
        self.titles.append(item.title)
        index = self.items.index(item)
        self.sku_lookup[item.sku] = index
        self.stock_id_lookup[item.stock_id] = index
        self.title_lookup[item.title] = index

    def extend(self, items):
        for item in items:
            self.append(item)
