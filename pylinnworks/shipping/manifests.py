from .. api_requests import GetManifests
from . manifest import Manifest


class Manifests:
    def __init__(self, api_session=None):
        self.api_session = api_session
        self.manifests = self.get_manifests()

    def __len__(self):
        return len(self.manifests)

    def __getitem__(self, index):
        return self.manifests[index]

    def __repr__(self):
        return 'Manifests Object'

    def get_manifests(self):
        request = GetManifests(self.api_session)
        manifests = [
            Manifest(self.api_session, data) for data
            in request.response_dict['Data']]
        return manifests

    def get_consignment_by_id(self, order_id):
        for manifest in self.manifests:
            try:
                return manifest.get_consignment_by_id(int(order_id))
            except ValueError:
                continue
        raise ValueError
