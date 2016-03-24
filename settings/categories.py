from . info_class import InfoClass
from . info_entry import InfoEntry
from linnapi.api_requests.settings.get_categories import GetCategories


class Categories(InfoClass):
    request_class = GetCategories
    name_field = 'CategoryName'
    id_field = 'CategoryId'
    info_list = []
