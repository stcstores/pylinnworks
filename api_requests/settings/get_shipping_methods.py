"""Requests shipping method information"""

from . get_info_request import GetInfoRequest


class GetShippingMethods(GetInfoRequest):
    url_extension = '/api/Orders/GetShippingMethods'
    info = []

    def get_info(self):
        """Return shipping_method information as dict."""
        info = []
        shipping_methods = []
        for service in self.response_dict:
            for method in service['PostalServices']:
                new_method = {}
                new_method['vendor'] = method['Vendor']
                new_method['id'] = method['pkPostalServiceId']
                new_method['tracking_required'] = method[
                    'TrackingNumberRequired']
                new_method['name'] = method['PostalServiceName']
                shipping_methods.append(new_method)
        return shipping_methods
