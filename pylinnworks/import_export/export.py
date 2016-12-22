from tabler import Tabler as Table
from .. api_requests import ExecuteCustomScriptCSV


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
