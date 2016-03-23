from . info_entry import InfoEntry
from . api_requests . functions import is_guid


class InfoClass:
    request_class = None
    entry_class = InfoEntry
    info_list = []
    name_field = ''
    id_field = ''

    def __init__(self, api_session):
        self.request = self.request_class(api_session)
        self.load_info()

    def load_info(self):
        for entry in self.request.response_dict:
            self.add_entry(entry)

    def add_entry(self, entry):
        self.info_list.append(
            self.entry_class(entry[self.id_field], entry[self.name_field]))

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.info_list[key]
        if isinstance(key, str):
            if is_guid(key):
                for entry in self.info_list:
                    if entry.guid == key:
                        return entry
            else:
                for entry in self.info_list:
                    if entry.name == key:
                        return entry
            raise ValueError
        raise KeyError
