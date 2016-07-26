import json
from simplejson.scanner import JSONDecodeError


class HTTPRequestError(Exception):
    def __init__(self, request):
        self.url = request.url
        try:
            self.response_text = json.dumps(
                request.json(), indent=4, sort_keys=True)
        except JSONDecodeError:
            self.response_text = request.text
        super().__init__(self.get_message())

    def get_message(self):
        raise NotImplementedError


class InvalidResponse(HTTPRequestError):
    def __init__(self, request):
        super().__init__(request)

    def get_message(self):
        message = "Request to " + self.url + "returned invalid response:\n"
        message += self.response_text
