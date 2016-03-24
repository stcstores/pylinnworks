from . info_class import InfoClass
from . info_entry import InfoEntry
from linnapi.api_requests.settings.get_locations import GetLocations


class Locations(InfoClass):
    request_class = GetLocations
    name_field = 'LocationName'
    id_field = 'StockLocationId'
    info_list = []
