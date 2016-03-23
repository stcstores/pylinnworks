"""Container object for open order information """

from . order_item import OrderItem as OrderItem
from . api_requests . orders . get_open_order import GetOpenOrder


class OpenOrder:
    order_id = None
    order_number = None
    customer_info = None
    folder_name = []
    external_reference_number = None
    hold_or_cancel = None
    invoice_printed = None
    label_error = None
    label_printed = None
    marker = None
    notes = None
    part_shipped = None
    pick_list_printed = None
    date_recieved = None
    time_recieved = None
    reference_number = None
    source = None
    status = None
    sub_source = None
    item_weight = None
    manual_adjust = None
    package_category = None
    postage_service = None
    package_type = None
    postage_cost = None
    postage_cost_ex_tax = None
    order_weight = None
    tracking_number = None
    country_tax_rate = None
    currency = None
    payment_method = None
    profit_margin = None
    subtotal = None
    tax = None
    total_charge = None
    total_discount = None
    items = []
    department = None

    def __init__(self, api_session, order_id=None, order_number=None,
                 customer_info=None, folder_name=None,
                 external_reference_number=None, hold_or_cancel=None,
                 invoice_printed=None, label_error=None, label_printed=None,
                 marker=None, notes=None, part_shipped=None,
                 pick_list_printed=None, date_recieved=None,
                 time_recieved=None, reference_number=None, channel=None,
                 status=None, item_weight=None, manual_adjust=None,
                 postage_service=None, package_group=None, postage_cost=None,
                 postage_cost_ex_tax=None, order_weight=None,
                 tracking_number=None, country_tax_rate=None, currency=None,
                 payment_method=None, payment_method_id=None,
                 profit_margin=None, subtotal=None, tax=None,
                 total_charge=None, total_discount=None, items=None):
        self.api_session = api_session
        if order_id is not None:
            self.order_id = order_id
        if order_number is not None:
            self.order_number = str(order_number)
        if customer_info is not None:
            self.customer_info = customer_info
        if folder_name is not None:
            self.foler_name = folder_name
        if external_reference_number is not None:
            self.external_reference_number = external_reference_number
        if hold_or_cancel is not None:
            self.hold_or_cancel = hold_or_cancel
        if invoice_printed is not None:
            self.invoice_printed = invoice_printed
        if label_error is not None:
            self.label_error = label_error
        if label_printed is not None:
            self.label_printed = label_printed
        if marker is not None:
            self.marker = marker
        if notes is not None:
            self.notes = notes
        if part_shipped is not None:
            self.part_shipped = part_shipped
        if pick_list_printed is not None:
            self.pick_list_printed = pick_list_printed
        if date_recieved is not None:
            self.date_recieved = date_recieved
        if time_recieved is not None:
            self.time_recieved = time_recieved
        if reference_number is not None:
            self.reference_number = reference_number
        if channel is not None:
            self.channel = channel
        if status is not None:
            self.status = status
        if item_weight is not None:
            self.item_weight = item_weight
        if manual_adjust is not None:
            self.manual_adjust = manual_adjust
        if package_group is not None:
            self.package_group = package_group
        if postage_service is not None:
            self.postage_service = postage_service
        if postage_cost is not None:
            self.postage_cost = postage_cost
        if postage_cost_ex_tax is not None:
            self.postage_cost_ex_tax = postage_cost_ex_tax
        if order_weight is not None:
            self.order_weight = order_weight
        if tracking_number is not None:
            self.tracking_number = tracking_number
        if country_tax_rate is not None:
            self.country_tax_rate = country_tax_rate
        if currency is not None:
            self.currency = currency
        if payment_method is not None:
            self.payment_method = payment_method
        if payment_method_id is not None:
            self.payment_method_id = payment_method_id
        if profit_margin is not None:
            self.profit_margin = profit_margin
        if subtotal is not None:
            self.subtotal = subtotal
        if tax is not None:
            self.tax = tax
        if total_charge is not None:
            self.total_charge = total_charge
        if total_discount is not None:
            self.total_discount = total_discount
        if items is not None:
            self.items = items

        self.department = self.get_order_department()

    def get_order_department(self):
        if len(self.items) == 0:
            department = "None"
        else:
            department = self.items[0].department
            for item in self.items:
                if item.department != department:
                    deparment = "Mixed"
                    break
        return department
