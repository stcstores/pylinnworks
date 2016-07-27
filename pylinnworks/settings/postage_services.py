import pylinnworks.api_requests as api_requests
from . info_class import InfoClass
from . info_entry import InfoEntry


class PostageServices(InfoClass):
    request_class = api_requests.GetPostageServices
    name_field = 'PostalServiceName'
    id_field = 'pkPostalServiceId'
    info_list = []
