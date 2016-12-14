

class ProcessedOrderList:
    def __init__(self, orders):
        self.orders = orders
        self.order_id_lookup = {order.order_id: order for order in self.orders}

    def __getitem__(self, index):
        return self.orders[index]

    def __len__(self):
        return len(self.orders)

    def __repr__(self):
        return 'ProcessedOrderList containing {} orders'.format(
            len(self.orders))

    def get_order_by_ID(self, order_id):
        return self.order_id_lookup[order_id]

    def get_orders_by_customer_name(self, customer_name):
        return ProcessedOrderList([
            order for order in self.orders if
            order.full_name == customer_name or
            order.channel_buyer_name == customer_name])

    def get_orders_by_customer_email(self, customer_email):
        return ProcessedOrderList([
            order for order in self.orders if order.email == customer_email])
