"""Requests category information"""

from . get_info_request import GetInfoRequest


class GetCategories(GetInfoRequest):
    url_extension = '/api/Inventory/GetCategories'
    info = []
    name_field = 'CategoryName'
    id_field = 'CategoryId'
