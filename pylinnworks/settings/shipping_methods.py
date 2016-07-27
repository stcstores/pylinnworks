import pylinnworks.api_requests as api_requests
from . info_class import InfoClass
from . info_entry import InfoEntry
from . shipping_method import ShippingMethod


class ShippingMethods(InfoClass):
    name = 'Shipping Methods'
    request_class = api_requests.GetShippingMethods
    entry_class = ShippingMethod
    info_list = []
    vendors = []
    vendor_lookup = {}

    def load_info(self):
        for service in self.request.response_dict:
            for entry in service['PostalServices']:
                vendor = service['Vendor']
                self.add_entry(entry, vendor)

    def add_entry(self, entry, vendor):
        new_entry = self.entry_class(
                entry['pkPostalServiceId'],
                entry['PostalServiceName'],
                vendor,
                entry['TrackingNumberRequired'])
        self.info_list.append(new_entry)
        new_entry_index = self.info_list.index(new_entry)
        self.ids.append(new_entry.guid)
        self.id_lookup[new_entry.guid] = new_entry_index
        self.names.append(new_entry.name)
        self.name_lookup[new_entry.name] = new_entry_index
        if new_entry.vendor not in self.vendors:
            self.vendors.append(new_entry.vendor)
        if new_entry.vendor not in self.vendor_lookup:
            self.vendor_lookup[new_entry.vendor] = []
        self.vendor_lookup[new_entry.vendor].append(new_entry_index)

    def __getitem__(self, key):
        if key in self.vendor_lookup:
            vendor_list = []
            for entry_index in self.vendor_lookup[key]:
                vendor_list.append(self.info_list[entry_index])
            return vendor_list
        elif key in self.id_lookup:
            return self.info_list[self.id_lookup[key]]
        elif key in self.names:
            return self.info_list[self.name_lookup[key]]
        else:
            return self.info_list[key]
