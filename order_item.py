from . inventory_item import InventoryItem as InventoryItem


class OrderItem:
    available = None
    barcode = None
    category = None
    channel_sku = None
    channel_title = None
    in_order_book = None
    stock_id = None
    item_number = None
    channel = None
    level = None
    quantity = None
    sku = None
    title = None
    weight = None

    def __init__(self, api_session,
                 available=None,
                 barcode=None,
                 category=None,
                 channel_sku=None,
                 channel_title=None,
                 in_order_book=None,
                 stock_id=None,
                 item_number=None,
                 channel=None,
                 level=None,
                 quantity=None,
                 sku=None,
                 title=None,
                 weight=None
                 ):
        self.api_session = api_session
        if available is not None:
            self.available = available
        if barcode is not None:
            self.barcode = barcode
        if category is not None:
            self.category = category
        if channel_sku is not None:
            self.channel_sku = channel_sku
        if channel_title is not None:
            self.channel_title = channel_title
        if in_order_book is not None:
            self.in_order_book = in_order_book
        if stock_id is not None:
            self.stock_id = stock_id
        if item_number is not None:
            self.item_number = item_number
        if channel is not None:
            self.channel = channel
        if level is not None:
            self.level = level
        if quantity is not None:
            self.quantity = quantity
        if sku is not None:
            self.sku = sku
        if title is not None:
            self.title = title
        if weight is not None:
            self.weight = weight

    def getInventoryItem(self, api_session):
        return InventoryItem(api_session, self.guid)
