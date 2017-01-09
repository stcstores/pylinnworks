import requests
from . exceptions import StatusError


class Request():
    url_server = None
    url_extension = ''
    data = {}
    response = None

    def __init__(self, api_session, test=True):
        self.test = test
        self.api_session = api_session
        if self.url_server is not None:
            self.url = self.url_server + self.url_extension
        else:
            self.url = self.api_session.server + self.url_extension
        self.data = self.get_data()
        if self.test is True:
            if self.test_request() is True:
                self.execute()
        else:
            self.execute()

    def execute(self):
        self.response = self.api_session.request(
            self.url,
            data=self.data,
            files=self.get_files(),
            params=self.get_params())
        self.json = self.response.text
        if self.test is True:
            if self.test_response(self.response) is True:
                self.load_respose_dict()
        else:
            self.load_respose_dict()

    def load_respose_dict(self):
        try:
            self.response_dict = self.response.json()
            self.process_response(self.response)
        except:
            pass

    def process_response(self, response):
        pass

    def test_request(self):
        return True

    def test_response(self, response):
        try:
            if not response.status_code // 100 == 2:
                raise StatusError(self, response, response.text)
        except requests.exceptions.RequestException as e:
            print('Sent to: {}'.format(self.request.url))
            print('Params: {}'.format(self.request.params))
            print('Data: {}'.format(self.request.data))
            raise
        return True

    def get_data(self):
        self.data = {}
        return self.data

    def get_files(self):
        return None

    def get_params(self):
        self.params = {}
        return self.params
