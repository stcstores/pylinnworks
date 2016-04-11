from linnapi.api_requests.settings.get_categories import GetCategories
from . info_class import InfoClass
from . info_entry import InfoEntry


class Categories(InfoClass):
    name = 'Categories'
    request_class = GetCategories
    name_field = 'CategoryName'
    id_field = 'CategoryId'
    info_list = []
