class StatusError(Exception):
    def __init__(self, request, response, message):
        print('Status: {}: {}'.format(response.status_code, response.reason))
        print(message)
        print('Sent to: {}'.format(response.url))
        print('Params: {}'.format(request.params))
        print('Data: {}'.format(request.data))
