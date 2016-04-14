"""Container object for open order information """

from linnapi.settings.info_entry import InfoEntry
import linnapi.api_requests as api_requests
from . order_item import OrderItem as OrderItem


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
    paid = None
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
    unlinked = None

    def __init__(self, api_session, order_id=None, order_number=None,
                 customer_info=None, folder_name=None,
                 external_reference_number=None, hold_or_cancel=None,
                 invoice_printed=None, label_error=None, label_printed=None,
                 marker=None, notes=None, part_shipped=None,
                 pick_list_printed=None, date_recieved=None,
                 time_recieved=None, reference_number=None, channel=None,
                 paid=None, item_weight=None, manual_adjust=None,
                 postage_service=None, package_group=None, postage_cost=None,
                 postage_cost_ex_tax=None, order_weight=None,
                 tracking_number=None, country_tax_rate=None, currency=None,
                 payment_method=None, payment_method_id=None,
                 profit_margin=None, subtotal=None, tax=None,
                 total_charge=None, total_discount=None, items=None,
                 unlinked=None, load_order_id=None):
        self.api_session = api_session
        if load_order_id is not None:
            self.load_from_order_id(load_order_id)
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
        if paid is not None:
            self.paid = paid
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
        if unlinked is not None:
            self.unlinked = unlinked

        self.category = self.get_order_category()
        if len(self.items) > 1:
            self.items.sort(key=lambda x: x.title)

    def get_order_category(self):
        if self.unlinked is True:
            return InfoEntry(None, 'UNLINKED')
        elif len(self.items) == 0:
            category = InfoEntry(None, "None")
        else:
            category = self.items[0].category
            for item in self.items:
                if item.category.guid != category.guid:
                    category = InfoEntry(None, "Mixed")
                    break
        return category

    def load_from_order_id(self, order_id, location=None):
        if location is None:
            location_id = self.api_session.locations['Default'].guid
        else:
            location_id = self.api_session.locations[location].guid
        self.request = api_requests.GetOpenOrders(
            self.api_session,
            count=99999,
            page_number=1,
            filters=None,
            location_id=location_id,
            additional_filter=None)
        order_data = None
        for order in self.request.response_dict['Data']:
            if order['OrderId'] == order_id:
                order_data = order
                break
        if order_data is None:
            raise ValueError('Order not in open orders.')
        else:
            self.load_from_request(order_data)

    def load_from_request(self, order_data):
        self.get_customer_info(order_data['CustomerInfo'])
        date_time = order_data['GeneralInfo']['ReceivedDate'].strip()
        self.date_recieved = date_time[:10]
        self.time_recieved = date_time[11:]
        channel_sub_source = order_data['GeneralInfo']['SubSource']
        if channel_sub_source in self.api_session.channels.sub_sources:
            self.channel = self.api_session.channels[channel_sub_source]
        else:
            self.channel = None
        self.items = self.get_items(order_data['Items'],  self.channel)
        if 'UNLINKED' in self.items:
            self.unlinked = True
        else:
            self.unlinked = False

        self.order_id = order_data['OrderId']
        self.order_number = str(order_data['NumOrderId'])
        self.folder_name = order_data['FolderName']
        self.external_reference_number = order_data[
            'GeneralInfo']['ExternalReferenceNum']
        self.hold_or_cancel = order_data['GeneralInfo']['HoldOrCancel']
        self.invoice_printed = order_data['GeneralInfo']['InvoicePrinted']
        self.label_error = order_data['GeneralInfo']['LabelError']
        self.label_printed = order_data['GeneralInfo']['LabelPrinted']
        self.marker = order_data['GeneralInfo']['Marker']
        self.notes = order_data['GeneralInfo']['Notes']
        self.part_shipped = order_data['GeneralInfo']['PartShipped']
        self.pick_list_printed = order_data['GeneralInfo']['PickListPrinted']
        self.reference_number = order_data['GeneralInfo']['ReferenceNum']
        self.paid = order_data['GeneralInfo']['Status']
        self.item_weight = order_data['ShippingInfo']['ItemWeight']
        self.manual_adjust = order_data['ShippingInfo']['ManualAdjust']
        self.postage_service = self.api_session.postage_services[
            order_data['ShippingInfo']['PostalServiceId']]
        self.package_group = self.api_session.package_groups[
            order_data['ShippingInfo']['PackageCategoryId']]
        self.postage_cost = order_data['ShippingInfo']['PostageCost']
        self.postage_cost_ex_tax = order_data[
            'ShippingInfo']['PostageCostExTax']
        self.order_weight = order_data['ShippingInfo']['TotalWeight']
        self.tracking_number = order_data['ShippingInfo']['TrackingNumber']
        self.country_tax_rate = order_data['TotalsInfo']['CountryTaxRate']
        self.currency = order_data['TotalsInfo']['Currency']
        self.payment_method = order_data['TotalsInfo']['PaymentMethod']
        self.payment_method_id = order_data['TotalsInfo']['PaymentMethodId']
        self.profit_margin = order_data['TotalsInfo']['ProfitMargin']
        self.subtotal = order_data['TotalsInfo']['Subtotal']
        self.tax = order_data['TotalsInfo']['Tax']
        self.total_charge = order_data['TotalsInfo']['TotalCharge']
        self.total_discount = order_data['TotalsInfo']['TotalDiscount']

    def get_customer_info(self, customer_data):
        self.address = [customer_data['Address']['Address1'],
                        customer_data['Address']['Address2'],
                        customer_data['Address']['Address3']]
        self.company = customer_data['Address']['Company']
        self.country = customer_data['Address']['Country']
        self.country_id = customer_data['Address']['CountryId']
        self.customer_email = customer_data['Address']['EmailAddress']
        self.customer_name = customer_data['Address']['FullName']
        self.customer_phone = customer_data['Address']['PhoneNumber']
        self.post_code = customer_data['Address']['PostCode']
        self.region = customer_data['Address']['Region']
        self.town = customer_data['Address']['Town']
        self.billing_address = customer_data['BillingAddress']
        self.customer_channel_name = customer_data['ChannelBuyerName']

    def get_items(self, item_data, channel):
        items = []
        for item in item_data:
            if item['SKU'] is None:
                new_item = 'UNLINKED'
            else:
                category = self.api_session.categories[item['CategoryName']]
                new_item = OrderItem(
                    self.api_session,
                    available=item['AvailableStock'],
                    barcode=item['BarcodeNumber'],
                    category=category,
                    channel_sku=item['ChannelSKU'],
                    channel_title=item['ChannelTitle'],
                    in_order_book=item['InOrderBook'],
                    stock_id=item['ItemId'],
                    item_number=item['ItemNumber'],
                    channel=channel,
                    level=item['Level'],
                    quantity=item['Quantity'],
                    sku=item['SKU'],
                    title=item['Title'],
                    weight=item['Weight'])
            items.append(new_item)
        return items

    def process(self):
        process_request = api_requests.ProcessOrder(
            self.api_session, self.order_id)
        return not self.is_open_order()

    def is_open_order(self):
        request = api_requests.GetOpenOrder(self.api_session, self.order_id)
        if 'GeneralInfo' in request.response_dict:
            return True
        else:
            return False
        return request

    def __str__(self):
        return "Order Number " + self.order_number
