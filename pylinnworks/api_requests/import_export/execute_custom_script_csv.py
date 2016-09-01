import json

from pylinnworks.api_requests.request import Request


class ExecuteCustomScriptCSV(Request):
    url_server = 'https://eu1.linnworks.net'
    url_extension = '/api/Dashboards/ExecuteCustomScriptCSV'

    def __init__(self, api_session, script_id, parameters=[]):
        self.script_id = script_id
        self.parameters = parameters
        super().__init__(api_session)

    def test_request(self):
        assert isinstance(self.script_id, (int, str))
        assert isinstance(self.parameters, list)
        return super().test_request()

    def get_data(self):
        data = {
            'parameters': json.dumps(self.parameters),
            'scriptId': self.script_id
        }
        return data

    def get_params(self):
        params = {
            'applicationName': 'Linnworks.net',
            'modleName': 'QueryData',
            'push': 'a4faccbe-7213-4340-a995-7bb9795fad43'}
        return params

    def test_response(self, response):
        return super().test_response(response)

    def process_response(self, response):
        self.export_url = self.response_dict
