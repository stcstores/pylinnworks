"""Uploads file to api.linnworks.net """

import os

from .. request import Request


class UploadFile(Request):
    url_extension = '/api/Uploader/UploadFile'
    params = {'type': 'Image', 'expiredInHours': '24'}

    def __init__(self, api, filepath, params=None):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)

    def get_params(self):
        return self.params

    def get_files(self):
        files = files = {self.filename: open(self.filepath, 'rb')}
