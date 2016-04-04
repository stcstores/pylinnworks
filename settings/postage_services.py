from linnapi.api_requests.settings.get_postage_services import\
    GetPostageServices
from . info_class import InfoClass
from . info_entry import InfoEntry


class PostageServices(InfoClass):
    request_class = GetPostageServices
    name_field = 'PostalServiceName'
    id_field = 'pkPostalServiceId'
    info_list = []
