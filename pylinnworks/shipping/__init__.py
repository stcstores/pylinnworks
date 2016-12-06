from pylinnworks.api_requests import GetManifests
from . manifest import Manifest


def get_manifests(api_session):
    request = GetManifests(api_session)
    manifests = [
        Manifest(api_session, data) for data in request.response_dict['Data']]
    return manifests
