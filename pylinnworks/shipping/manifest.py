from . previous_manifest import PreviousManifest
from . manifest_shipping_service import ManifestShippingService


class Manifest:
    def __init__(self, api_session, data):
        self.api_session = api_session
        self.account_id = data['AccountId']
        self.average_weight = data['AverageWeight']
        self.consignments_defferred = data['ConsignmentsDeferred']
        self.external_manifest_id = data['ExternalManifestId']
        self.is_complete = data['IsComplete']
        self.is_error = data['IsError']
        self.manifest_id = data['ManifestId']
        self.total_consignments = data['TotalConsignments']
        self.total_weight = data['TotalWeight']
        self.vendor = data['Vendor']
        self.services = [
            ManifestShippingService(self.api_session, self, service) for
            service in data['Services']]
        if data['PreviousManifest'] is not None:
            self.previous_manifest = PreviousManifest(
                self.api_session, self, data['PreviousManifest'])

    def __repr__(self):
        return 'Manifest: {} {}'.format(self.manifest_id, self.vendor)

    def __len__(self):
        return len(self.services)

    def __getitem__(self, index):
        return self.services[index]

    def get_consignment_by_id(self, order_id):
        for service in self.services:
            try:
                return service.get_consignment_by_id(order_id)
            except ValueError:
                continue
        raise ValueError

    def get_consignments(self):
        consignments = []
        for service in self.services:
            for consignment in service.consignments:
                consignments.append(consignment)
        return consignments
