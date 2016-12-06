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

    def get_consignments(self):
        request = GetConsigments(
            self.api_session, self.manifest.vendor, self.service_id,
            self.manifest.account_id)
        consignments = [Consignment(self.manifest, self, data) for data in
                        request.response_dict['Data']]
        return consignments
