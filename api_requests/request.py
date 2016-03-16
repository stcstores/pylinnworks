class Request():
    url_extension = ''
    data = {}
    response = None

    def __init__(self, api):
        self.api = api
        self.url = self.api.server + self.url_extension
        self.execute()

    def execute(self):
        self.response = self.api.request(self.url, data=self.get_data())
        self.json = self.response.text
        try:
            self.response_dict = self.response.json()
        except:
            self.response_dict = None
        self.process_response(self.response)

    def process_response(self, response):
        pass

    def get_data(self):
        data = {}
        self.data = data
        return data
