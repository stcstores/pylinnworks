"""Requests extended property names """

from .. request import Request


class GetExtendedPropertyNames(Request):
    url_extension = '/api/Inventory/GetExtendedPropertyNames'
