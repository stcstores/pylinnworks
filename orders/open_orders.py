from linnapi.api_requests.orders.get_open_orders import GetOpenOrders
from linnapi.api_requests.orders.create_PDF_from_job_force_template\
    import CreatePDFFromJobForceTemplate
from linnapi.api_requests.orders.get_print_file import GetPrintFile
from . open_order import OpenOrder
from . order_item import OrderItem


class OpenOrders:

    def __init__(self, api_session, load=False, location='Default',
                 orders=None):
        self.location = location
        self.orders = []
        self.numbers = []
        self.ids = []
        self.number_lookup = {}
        self.id_lookup = {}
        self.api_session = api_session
        if orders is not None:
            self.orders = orders
            self.update()
        elif load is True:
            self.load()

    def append(self, order):
        self.orders.append(order)
        self.update()

    def item_count(self):
        count = 0
        for order in self.orders:
            count += len(order.items)
        return count

    def load(self):
        location_id = self.api_session.locations[self.location].guid
        self.request = GetOpenOrders(
            self.api_session,
            count=99999,
            page_number=1,
            filters=None,
            location_id=location_id,
            additional_filter=None)
        for order in self.request.response_dict['Data']:
            self.add_order(order)
        self.update()

    def update(self):
        self.numbers = []
        self.ids = []
        self.number_lookup = {}
        self.id_lookup = {}
        for order in self.orders:
            order_index = self.orders.index(order)
            self.numbers.append(order.order_number)
            self.ids.append(order.order_id)
            self.number_lookup[order.order_number] = order_index
            self.id_lookup[order.order_id] = order_index





    def add_order(self, order_data):
        new_order = OpenOrder(self.api_session)
        new_order.load_from_request(order_data)
        self.ids.append(new_order.order_id)
        self.numbers.append(new_order.order_number)
        self.orders.append(new_order)
        new_order_index = self.orders.index(new_order)
        self.id_lookup[new_order.order_id] = new_order_index
        self.number_lookup[new_order.order_number] = new_order_index

    def __getitem__(self, key):
        if key in self.ids:
            return self.orders[self.id_lookup[key]]
        elif key in self.numbers:
            return self.orders[self.number_lookup[key]]
        else:
            return self.orders[key]

    def __iter_(self):
        for order in self.orders:
            yield order

    def __len__(self):
        return len(self.orders)

    def print_pick_list(self, printer_name):
        self.print_orders('Pick List', printer_name)

    def print_orders(self, template, printer_name):
        import printer
        printer = printer.Printer(printer_name=printer_name)
        order_ids = []
        for order in self.orders:
            order_ids.append(order.order_id)
        request = CreatePDFFromJobForceTemplate(
            self.api_session, ids=order_ids, printer_name='PDF',
            template_type=template)
        print(request.data)
        print_file = GetPrintFile(self.api_session, request.url)
        printer.print_content(print_file.file)
