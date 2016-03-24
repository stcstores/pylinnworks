from .open_orders import OpenOrders


class PrintList:
    invoice_printer = None
    pack_list_printer = None
    pick_list_printer = None
    shipping_label_printer = None
    print_invoice = False
    print_pack_list = False
    print_pick_list = False
    print_shipping_label = False
    paid = None
    invoice_printed = None
    shipping_label_printed = None
    pick_list_printed = None
    categories = None
    countries = None
    shipping_services = None
    location = None
    unlinked = None
    batch = False

    def __init__(self, api_session):
        self.api_session = api_session
        self.all_open_orders = OpenOrders(api_session, load=True,
                                          location=self.location)
        self.print_lists = []
        orders_to_print = []
        for order in self.all_open_orders:
            if self.order_to_be_printed(order):
                orders_to_print.append(order)
        self.orders_to_print = OpenOrders(api_session, orders=orders_to_print)
        self.separated_orders = self.separate_orders(self.orders_to_print)
        self.sorted_orders = []
        for order_list in self.separated_orders:
            self.sorted_orders.append(self.sort_orders(order_list))
        if self.batch is True:
            for order_list in self.sorted_orders:
                batch = self.batch(order_list)
                self.print_lists.append(batch)
        else:
            self.print_lists = self.separated_orders

    def separate_orders(self, orders):
        return [orders]

    def sort_orders(self, orders):
        return orders

    def order_to_be_printed(self, order):
        if self.paid is not None:
            if order.paid != self.paid:
                return False
        if self.invoice_printed is not None:
            if order.invoice_printed != self.invoice_printed:
                return False
        if self.shipping_label_printed is not None:
            if order.shipping_label_printed != self.shipping_label_printed:
                return False
        if self.pick_list_printed is not None:
            if order.pick_list_printed != self.pick_list_printed:
                return False
        if self.unlinked is not None:
            if order.unlinked != self.unlinked:
                return False
        if self.categories is not None:
            if order.category.name not in self.categories:
                return False
        if self.countries is not None:
            if order.country not in self.countries:
                return False
        if self.shipping_services is not None:
            if order.shipping_service.name not in self.shipping_services:
                return False
        return True

    def batch(self, orders):
        NotImplemented

    def print_orders(self):
        for print_list in self.print_lists:
            if self.print_pick_list is True:
                print_list.print_pick_list(printer=self.pick_list_printer)
            if self.print_pack_list is True:
                print_list.print_pack_list(printer=self.pack_list_printer)
            if self.print_shipping_label is True:
                print_list.print_shipping_label(
                    printer=self.shipping_label_printer)
