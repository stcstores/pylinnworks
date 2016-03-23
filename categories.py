from . info_class import InfoClass
from . info_entry import InfoEntry
from . api_requests . info . get_categories import GetCategories


class Categories(InfoClass):
    request_class = GetCategories
    name_field = 'CategoryName'
    id_field = 'CategoryId'
    info_list = []
