from datetime import timedelta
from datetime import datetime

from pylinnworks import api_requests
from . exceptions import SearchFieldNotFound
from . processed_order_list import ProcessedOrderList
from . processed_order import ProcessedOrder
from .. pylinnworks import PyLinnworks


class ProcessedOrders(PyLinnworks):
    search_types = ('PROCESSED', 'ALLDATES', 'RECEIVED' 'PAYMENTRECIEVED')
    default_search_type = 'RECIEVED'
    default_from_date = datetime.today()
    default_to_date = datetime.today() + timedelta(days=1)

    def __init__(self):
        self.set_search_columns()
        self.search_fields = SearchFields(self.api_session)
        self.default_search_field = self.search_fields.get('Order ID')

    def __repr__(self):
        return 'ProcessedOrders Object'

    @classmethod
    def request_orders(
            cls, search_term, from_date, to_date, exact_match, date_type,
            page_num):
        from_date = cls.make_request_date(from_date)
        to_date = cls.make_request_date(to_date)
        request = api_requests.SearchProcessedOrdersPaged(
            cls, search_term=search_term, from_date=from_date,
            to_date=to_date, exact_match=exact_match, date_type=date_type,
            page_num=page_num)
        return request

    @staticmethod
    def make_request_date(day):
        return '{}-{}-{} 0:0:0'.format(day.month, day.day, day.year)

    @classmethod
    def get_order_data(
            cls, search_term, from_date, to_date, exact_match, date_type):
        request = cls.request_orders(
            search_term, from_date, to_date, exact_match, date_type, 1)
        data = request.response_dict['Data']
        for page in range(2, request.response_dict['TotalPages'] + 1):
            request = cls.request_orders(
                search_term, from_date, to_date, exact_match, date_type, page)
            data += request.response_dict['Data']
        return [ProcessedOrder(order_data) for order_data in data]

    @classmethod
    def search_processed_orders(
            cls, search_term='', from_date=None, to_date=None,
            exact_match=True, date_type=None):
        order_data = cls.get_order_data(
            search_term, from_date, to_date, exact_match, date_type)
        orders = ProcessedOrderList(order_data)
        return orders

    @classmethod
    def get_all_processed_orders_between(cls, from_date, to_date, date_type):
        return cls.search_processed_orders(
            from_date=from_date, to_date=to_date, date_type=date_type)

    @classmethod
    def get_all_processed_orders_for_day(cls, day, date_type):
        from_date = day
        to_date = day + timedelta(days=1)
        return cls.search_processed_orders(
            from_date=from_date, to_date=to_date, date_type=date_type)

    @classmethod
    def set_search_columns(cls):
        api_requests.SetColumns(cls)

    @classmethod
    def count_orders(cls, from_date, to_date, date_type):
        request = cls.request_orders(
            '', from_date, to_date, True, date_type, 1)
        return request.response_dict['TotalEntries']

    @classmethod
    def count_orders_for_day(cls, date, date_type):
        return cls.count_orders(date, date + timedelta(days=1), date_type)


class SearchFields:
    def __init__(self, api_session):
        self.api_session = api_session
        self.search_fields = self.get_search_fields()

    def __getitem__(self, index):
        return self.search_fields[index]

    def get_search_fields(self):
        request = api_requests.GetSearchTypes(self.api_session)
        search_fields = [SearchField(data) for data in request.response_dict]
        return search_fields

    def get(self, search_term):
        for field in self.search_fields:
            if field.name.lower() == search_term.lower():
                return field
        for field in self.search_fields:
            if field.field.lower() == search_term.lower():
                return field
        raise SearchFieldNotFound(search_term)


class SearchField:
    def __init__(self, data):
        self.name = data['Name']
        self.field = data['Field']
        self.allow_for_all_dates = data['AllowForAllDates']
        self.exact_search_optional = data['ExactSearchOptional']

    def __str__(self):
        return self.name
