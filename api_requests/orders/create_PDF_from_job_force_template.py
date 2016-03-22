import requests
from .. request import Request


class CreatePDFFromJobForceTemplate(Request):
    url_extension = '/api/PrintService/CreatePDFfromJobForceTemplate'
    printer_name = 'PDF'
    template_type = 'Invoice Template'
    ids = []

    def __init__(self, api_session, ids=None, printer_name=None,
                 template_type=None):
        if ids is not None:
            self.ids = ids
        if printer_name is not None:
            self.printer_name = printer_name
        if template_type is not None:
            self.template_type = template_type
        super().__init__(api_session)

    def processs_response(self, response):
        self.ids_processed = self.response_dict['IdsProcessed']
        self.print_errors = self.response_dict['PrintErrors']
        self.response_url = self.response_dict['URL']

    def save_pdf(self, filename):
        response = requests.get(self.response_url)
        with open(filename, "w") as out_file:
            out_file.write(response.text)
