from . info_class import InfoClass
from . info_entry import InfoEntry
from . api_requests . info . get_shipping_methods import GetShippingMethods
from . shipping_method import ShippingMethod


class ShippingMethods(InfoClass):
    request_class = GetShippingMethods
    entry_class = ShippingMethod
    info_list = []

    def load_info(self):
        for service in self.request.response_dict:
            for entry in service['PostalServices']:
                vendor = service['Vendor']
                self.add_entry(entry, vendor)

    def add_entry(self, entry, vendor):
        self.info_list.append(
            self.entry_class(
                entry['pkPostalServiceId'],
                entry['PostalServiceName'],
                vendor,
                entry['TrackingNumberRequired']))
