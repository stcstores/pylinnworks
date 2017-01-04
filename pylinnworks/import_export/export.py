from tabler import Tabler as Table
from .. api_requests import ExecuteCustomScriptCSV
from .. pylinnworks import PyLinnworks


class Export(PyLinnworks):
    def __init__(self, api_session):
        self.api_session = api_session

    @classmethod
    def get_export(cls, script_id, parameters=[]):
        request = ExecuteCustomScriptCSV(
            cls, script_id, parameters)
        table = Table()
        table.open_url(request.export_url)
        return table

    @classmethod
    def get_linking(cls):
        table = cls.get_export(14)
        return table

    @classmethod
    def get_orders_between_dates(cls, start_date, end_date):
        script_id = 9
        start = cls.linnworks_time(start_date)
        end = cls.linnworks_time(end_date)
        parameters = [
            {'Type': 'Date', 'Name': 'startDate', 'Value': start},
            {'Type': 'Date', 'Name': 'endDate', 'Value': end}]
        return cls.get_export(script_id, parameters=parameters)

    @classmethod
    def get_inventory(cls, location='Default'):
        parameters = [
            {"Type": "Select", "Name": "locationName", "Value": location}]
        cls.get_export(script_id=8, parameters=parameters)

    @classmethod
    def get_extended_properties(cls, sku='', property=''):
        parameters = [
            {"Type": "String", "Name": "SKU", "Value": ""},
            {"Type": "String", "Name": "Property", "Value": ""}]
        cls.get_export(script_id=57, parameters=parameters)
