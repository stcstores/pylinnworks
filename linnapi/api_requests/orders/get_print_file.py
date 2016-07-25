

class GetPrintFile:
    def __init__(self, api_session, url):
        self.api_session = api_session
        self.response = self.api_session.request(url)
        self.file = self.response.content
