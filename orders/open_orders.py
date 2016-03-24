from . open_order import OpenOrder
from . order_item import OrderItem
from . customer_info import CustomerInfo
from linnapi.settings.categories import Categories
from linnapi.settings.locations import Locations
from linnapi.settings.postage_services import PostageServices
from linnapi.settings.package_groups import PackageGroups
from linnapi.settings.channels import Channels
from linnapi.api_requests.orders.get_open_orders import GetOpenOrders


class OpenOrders:

    def __init__(self, api_session, load=False, location='Default',
                 orders=None):
        self.location = location
        self.categories = Categories(api_session)
        self.postage_services = PostageServices(api_session)
        self.package_groups = PackageGroups(api_session)
        self.channels = Channels(api_session)
        self.locations = Locations(api_session)
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
        location_id = self.locations[self.location].guid
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

    def get_items(self, item_data, channel):
        items = []
        for item in item_data:
            if item['SKU'] is None:
                new_item = 'UNLINKED'
            else:
                category = self.categories[item['CategoryName']]
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

    def get_customer_info(self, customer_data):
        address = [customer_data['Address']['Address1'],
                   customer_data['Address']['Address2'],
                   customer_data['Address']['Address3']]
        company = customer_data['Address']['Company']
        country = customer_data['Address']['Country']
        country_id = customer_data['Address']['CountryId']
        email = customer_data['Address']['EmailAddress']
        name = customer_data['Address']['FullName']
        phone = customer_data['Address']['PhoneNumber']
        post_code = customer_data['Address']['PostCode']
        region = customer_data['Address']['Region']
        town = customer_data['Address']['Town']
        billing_address = customer_data['BillingAddress']
        channel_name = customer_data['ChannelBuyerName']
        return CustomerInfo(address=address, company=company, country=country,
                            country_id=country_id, email=email, name=name,
                            phone=phone, post_code=post_code, region=region,
                            town=town, billing_address=billing_address,
                            channel_name=channel_name)

    def add_order(self, order_data):
        customer_info = self.get_customer_info(order_data['CustomerInfo'])
        date_time = order_data['GeneralInfo']['ReceivedDate'].strip()
        channel_sub_source = order_data['GeneralInfo']['SubSource']
        if channel_sub_source in self.channels.sub_sources:
            channel = self.channels[channel_sub_source]
        else:
            channel = None
        date_recieved = date_time[:10]
        time_recieved = date_time[11:]
        items = self.get_items(order_data['Items'],  channel)
        if 'UNLINKED' in items:
            unlinked = True
        else:
            unlinked = False

        new_order = OpenOrder(
            self.api_session,
            order_id=order_data['OrderId'],
            order_number=order_data['NumOrderId'],
            customer_info=customer_info,
            folder_name=order_data['FolderName'],
            external_reference_number=order_data[
                'GeneralInfo']['ExternalReferenceNum'],
            hold_or_cancel=order_data['GeneralInfo']['HoldOrCancel'],
            invoice_printed=order_data['GeneralInfo']['InvoicePrinted'],
            label_error=order_data['GeneralInfo']['LabelError'],
            label_printed=order_data['GeneralInfo']['LabelPrinted'],
            marker=order_data['GeneralInfo']['Marker'],
            notes=order_data['GeneralInfo']['Notes'],
            part_shipped=order_data['GeneralInfo']['PartShipped'],
            pick_list_printed=order_data['GeneralInfo']['PickListPrinted'],
            date_recieved=date_recieved,
            time_recieved=time_recieved,
            reference_number=order_data['GeneralInfo']['ReferenceNum'],
            channel=channel,
            paid=order_data['GeneralInfo']['Status'],
            item_weight=order_data['ShippingInfo']['ItemWeight'],
            manual_adjust=order_data['ShippingInfo']['ManualAdjust'],
            postage_service=self.postage_services[
                order_data['ShippingInfo']['PostalServiceId']],
            package_group=self.package_groups[
                order_data['ShippingInfo']['PackageCategoryId']],
            postage_cost=order_data['ShippingInfo']['PostageCost'],
            postage_cost_ex_tax=order_data[
                'ShippingInfo']['PostageCostExTax'],
            order_weight=order_data['ShippingInfo']['TotalWeight'],
            tracking_number=order_data['ShippingInfo']['TrackingNumber'],
            country_tax_rate=order_data['TotalsInfo']['CountryTaxRate'],
            currency=order_data['TotalsInfo']['Currency'],
            payment_method=order_data['TotalsInfo']['PaymentMethod'],
            payment_method_id=order_data['TotalsInfo']['PaymentMethodId'],
            profit_margin=order_data['TotalsInfo']['ProfitMargin'],
            subtotal=order_data['TotalsInfo']['Subtotal'],
            tax=order_data['TotalsInfo']['Tax'],
            total_charge=order_data['TotalsInfo']['TotalCharge'],
            total_discount=order_data['TotalsInfo']['TotalDiscount'],
            items=items, unlinked=unlinked)
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
