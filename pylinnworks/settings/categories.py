import pylinnworks.api_requests as api_requests
from . info_class import InfoClass


class Categories(InfoClass):
    name = 'Categories'
    request_class = api_requests.GetCategories
    name_field = 'CategoryName'
    id_field = 'CategoryId'
    info_list = []
