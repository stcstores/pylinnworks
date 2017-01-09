class StatusError(Exception):

    def __init__(self, request, response, request_message):
        message = "\n".join([
            'Status: {}: {}'.format(response.status_code, response.reason),
            request_message,
            'Sent to: {}'.format(response.url),
            'Params: {}'.format(request.params),
            'Data: {}'.format(request.data)])
        super().__init__(message)


class RequestException(Exception):

    def __init__(request, original_exception):
        message = "\n".join([
            'Sent to: {}'.format(request.request.url),
            'Params: {}'.format(request.request.params),
            'Data: {}'.format(request.request.data)])
        super.__init__(message)
