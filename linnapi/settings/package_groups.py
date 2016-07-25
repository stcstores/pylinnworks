import linnapi.api_requests as api_requests
from . info_class import InfoClass
from . info_entry import InfoEntry


class PackageGroups(InfoClass):
    name = 'Package Groups'
    request_class = api_requests.GetPackageGroups
    name_field = 'Key'
    id_field = 'Value'
    info_list = []
