import linnapi.api_requests as api_requests
from . info_class import InfoClass
from . info_entry import InfoEntry


class Locations(InfoClass):
    name = 'Locations'
    request_class = api_requests.GetLocations
    name_field = 'LocationName'
    id_field = 'StockLocationId'
    info_list = []
