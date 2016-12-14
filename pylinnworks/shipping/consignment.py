from .. api_requests import CancelConsignment


class Consignment:
    def __init__(self, api_session, manifest, service, data):
        self.api_session = api_session
        self.service = manifest
        self.manifest = service
        self.consignment_id = data['ConsignmentId']
        self.country = data['Country']
        self.customer = data['Customer']
        self.deferred = data['Deferred']
        self.email = data['Email']
        self.order_id = data['OrderId']
        self.packages = data['Packages']
        self.postal_code = data['PostalCode']
        self.tracking_numbers = data['TrackingNumbers']
        self.weight = data['Weight']

    def __repr__(self):
        return 'Consignment: {}'.format(self.order_id)

    def cancel(self):
        request = CancelConsignment(
            self.api_session, self.manifest.vendor, self.manifest.account_id,
            self.consignment_id, self.order_id)
