from . info_class import InfoClass
from . info_entry import InfoEntry
from . api_requests . info . get_package_groups import GetPackageGroups


class PackageGroups(InfoClass):
    request_class = GetPackageGroups
    name_field = 'Key'
    id_field = 'Value'
    info_list = []
