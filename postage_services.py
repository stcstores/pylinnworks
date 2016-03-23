from . info_class import InfoClass
from . info_entry import InfoEntry
from . api_requests . info . get_postage_services import GetPostageServices


class PostageServices(InfoClass):
    request_class = GetPostageServices
    name_field = 'PostalServiceName'
    id_field = 'pkPostalServiceId'
    info_list = []
