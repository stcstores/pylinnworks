from .. api_requests import GetManifests
from . manifest import Manifest
from .. pylinnworks import PyLinnworks


class Manifests(PyLinnworks):
    def __init__(self, api_session=None):
        self.api_session = api_session
        self.manifests = self.get_manifests()

    def __len__(self):
        return len(self.manifests)

    def __getitem__(self, index):
        return self.manifests[index]

    def __repr__(self):
        return 'Manifests Object'

    @classmethod
    def get_manifests(cls):
        request = GetManifests(cls)
        manifests = [
            Manifest(cls, data) for data
            in request.response_dict['Data']]
        return manifests

    def get_consignment_by_id(self, order_id):
        for manifest in self.manifests:
            try:
                return manifest.get_consignment_by_id(int(order_id))
            except ValueError:
                continue
        raise ValueError

    def get_consignments(self):
        consignments = []
        for manifest in self.manifests:
            for consignment in manifest.get_consignments():
                consignments.append(consignment)
        return consignments
