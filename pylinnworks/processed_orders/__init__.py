from pylinnworks import LinnworksAPISession
from pylinnworks import api_requests
from . processed_order import ProcessedOrder
from datetime import timedelta
from datetime import datetime
from . exceptions import SearchFieldNotFound


class ProcessedOrders:
    search_types = ('PROCESSED', 'ALLDATES', 'RECEIVED' 'PAYMENTRECIEVED')
    default_search_type = 'RECIEVED'
    default_from_date = datetime.today()
    default_to_date = datetime.today() + timedelta(days=1)

    def __init__(self, api_session=None):
        if api_session is None:
            self.api_session = LinnworksAPISession()
        else:
            self.api_session = api_session
        self.set_search_columns()
        self.search_fields = SearchFields(self.api_session)
        self.default_search_field = self.search_fields.get('Order ID')

    def request_orders(
            self, search_term, from_date, to_date, exact_match, date_type,
            page_num):
        from_date = self.make_request_date(from_date)
        to_date = self.make_request_date(to_date)
        request = api_requests.SearchProcessedOrdersPaged(
            self.api_session, search_term=search_term, from_date=from_date,
            to_date=to_date, exact_match=exact_match, date_type=date_type,
            page_num=page_num)
        return request

    def make_request_date(self, day):
        return '{}-{}-{} 0:0:0'.format(day.month, day.day, day.year)

    def get_order_data(
            self, search_term, from_date, to_date, exact_match, date_type):
        request = self.request_orders(
            search_term, from_date, to_date, exact_match, date_type, 1)
        data = request.response_dict['Data']
        for page in range(2, request.response_dict['TotalPages'] + 1):
            request = self.request_orders(
                search_term, from_date, to_date, exact_match, date_type, page)
            data += request.response_dict['Data']
        return [ProcessedOrder(order_data) for order_data in data]

    def search_processed_orders(
            self, search_term='', from_date=None, to_date=None,
            exact_match=True, date_type=None):
        order_data = self.get_order_data(
            search_term, from_date, to_date, exact_match, date_type)
        orders = ProcessedOrderList(order_data)
        return orders

    def get_all_processed_orders_between(self, from_date, to_date, date_type):
        return self.search_processed_orders(
            from_date=from_date, to_date=to_date, date_type=date_type)

    def get_all_processed_orders_for_day(self, day, date_type):
        from_date = day
        to_date = day + timedelta(days=1)
        return self.search_processed_orders(
            from_date=from_date, to_date=to_date, date_type=date_type)

    def set_search_columns(self):
        api_requests.SetColumns(self.api_session)

    def count_orders(self, from_date, to_date, date_type):
        request = self.request_orders(
            '', from_date, to_date, True, date_type, 1)
        return request.response_dict['TotalEntries']

    def count_orders_for_day(self, date, date_type):
        return self.count_orders(date, date + timedelta(days=1), date_type)


class ProcessedOrderList:
    def __init__(self, orders):
        self.orders = orders
        self.order_id_lookup = {order.order_id: order for order in self.orders}

    def __getitem__(self, index):
        return self.orders[index]

    def __len__(self):
        return len(self.orders)

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


class SearchFields:
    def __init__(self, api_session):
        self.api_session = api_session
        self.search_fields = {
            search_field.name.lower(): search_field for search_field in
            self.get_search_fields()}

    def get_search_fields(self):
        request = api_requests.GetSearchTypes(self.api_session)
        search_fields = [SearchField(data) for data in request.response_dict]
        return search_fields

    def get(self, search_term):
        if search_term.lower() in self.search_fields:
            return self.search_fields[search_term.lower()]
        for name, field in self.search_fields.items():
            if field.field.lower() == search_term.lower():
                return field
        raise SearchFieldNotFound(search_term)


class SearchField:
    def __init__(self, data):
        self.name = data['Name']
        self.field = data['Field']
        self.allow_for_all_dates = data['AllowForAllDates']
        self.exact_search_optional = data['ExactSearchOptional']
