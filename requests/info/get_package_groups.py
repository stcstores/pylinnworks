"""Requests package group information"""

from . get_info_request import GetInfoRequest


class GetPackageGroups(GetInfoRequest):
    url_extension = '/api/Inventory/GetPackageGroups'
    info = []
    name_field = 'Key'
    id_field = 'Value'
