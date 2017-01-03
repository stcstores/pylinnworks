from tabler import Tabler as Table
from .. api_requests import ExecuteCustomScriptCSV
from .. functions import linnworks_datetime


class Export:
    def __init__(self, api_session):
        self.api_session = api_session

    def get_export(self, script_id, parameters=[]):
        request = ExecuteCustomScriptCSV(
            self.api_session, script_id, parameters)
        table = Table()
        table.open_url(request.export_url)
        return table

    def get_linking_table(self):
        table = self.get_export(14)
        return table

    def get_orders_between_dates(self, start_date, end_date):
        script_id = 9
        start = linnworks_datetime(start_date)
        end = linnworks_datetime(end_date)
        parameters = [
            {'Type': 'Date', 'Name': 'startDate', 'Value': start},
            {'Type': 'Date', 'Name': 'endDate', 'Value': end}]
        return self.get_export(script_id, parameters=parameters)
