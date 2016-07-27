"""Uploads file to api.linnworks.net """

import os

from pylinnworks.api_requests.request import Request


class UploadFile(Request):
    url_extension = '/api/Uploader/UploadFile'

    def __init__(
            self, api_session, filepath, file_type='Image', expire_in=24,
            test=True):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.type = file_type
        self.expire_in = expire_in
        super().__init__(api_session, test=test)

    def get_params(self):
        return {'type': self.type, 'expiredInHours': str(self.expire_in)}

    def get_files(self):
        files = {self.filename: open(self.filepath, 'rb')}
        return files
