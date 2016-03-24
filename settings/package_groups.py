from . info_class import InfoClass
from . info_entry import InfoEntry
from linnapi.api_requests.settings.get_package_groups import GetPackageGroups


class PackageGroups(InfoClass):
    request_class = GetPackageGroups
    name_field = 'Key'
    id_field = 'Value'
    info_list = []
