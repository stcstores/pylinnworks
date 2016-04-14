import linnapi.api_requests as api_requests
from . info_class import InfoClass
from . info_entry import InfoEntry


class Categories(InfoClass):
    name = 'Categories'
    request_class = api_requests.GetCategories
    name_field = 'CategoryName'
    id_field = 'CategoryId'
    info_list = []
