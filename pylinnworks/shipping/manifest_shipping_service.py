from pylinnworks.api_requests import GetConsigments
from . consignment import Consignment


class ManifestShippingService:
    def __init__(self, api_session, manifest, data):
        self.api_session = api_session
        self.manifest = manifest
        self.deferred_consignments = data['DeferredConsignments']
        self.manifest_average_weight = data['ManifestAverageWeight']
        self.manifest_consignments = data['ManifestConsignments']
        self.manifest_total_weight = data['ManifestTotalWeight']
        self.service_group = data['ServiceGroup']
        self.service_id = data['ServiceId']
        self.service_name = data['ServiceName']
        self.consignments = self.get_consignments()

    def __repr__(self):
        return 'ManifestShippingService: {}'.format(self.service_name)

    def __getitem__(self, index):
        return self.consignments[index]

    def __len__(self):
        return len(self.consignments)

    def get_consignments(self):
        request = GetConsigments(
            self.api_session, self.manifest.vendor, self.service_id,
            self.manifest.account_id)
        consignments = [
            Consignment(self.api_session, self.manifest, self, data) for data
            in request.response_dict['Data']]
        return consignments

    def get_consignment_by_id(self, order_id):
        for consignment in self.consignments:
            if consignment.order_id == order_id:
                return consignment
        raise ValueError
