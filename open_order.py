from . order_item import OrderItem as OrderItem


class OpenOrder:

    def __init__(self, order_data):
        self.order_id = order_data['OrderId']
        self.order_number = order_data['NumOrderId']
        self.customer_name = order_data['CustomerInfo']['Address']['FullName']
        self.printed = order_data['GeneralInfo']['InvoicePrinted']
        self.postage_service = order_data['ShippingInfo']['PostalServiceName']
        date_time = order_data['GeneralInfo']['ReceivedDate'].strip()
        self.date_recieved = date_time[:10]
        self.time_recieved = date_time[11:]
        self.items = []
        for item_data in order_data['Items']:
            self.items.append(OrderItem(item_data))
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
