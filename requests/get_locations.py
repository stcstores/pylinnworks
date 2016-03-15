"""Requests location information"""

from . get_info_request import GetInfoRequest


class GetLocations(GetInfoRequest):
    url_extension = '/api/Inventory/GetStockLocations'
    info = []
    name_field = 'LocationName'
    id_field = 'StockLocationId'
