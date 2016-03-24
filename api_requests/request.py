class Request():
    url_extension = ''
    data = {}
    response = None

    def __init__(self, api_session):
        self.api_session = api_session
        self.url = self.api_session.server + self.url_extension
        self.data = self.get_data()
        if self.test_request():
            self.execute()

    def execute(self):
        self.response = self.api_session.request(
                                                 self.url,
                                                 data=self.data,
                                                 files=self.get_files(),
                                                 params=self.get_params())
        #self.response.raise_for_status()
        self.json = self.response.text
        if self.test_response(self.response):
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
        return True

    def get_data(self):
        data = {}
        return data

    def get_files(self):
        return None

    def get_params(self):
        return {}
