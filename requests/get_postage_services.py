"""Requests postage service information"""

from . get_info_request import GetInfoRequest


class GetPostageServices(GetInfoRequest):
    url_extension = '/api/PostalServices/GetPostalServices'
    info = []
    name_field = 'PostalServiceName'
    id_field = 'pkPostalServiceId'
