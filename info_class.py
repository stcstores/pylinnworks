from . info_entry import InfoEntry
from . api_requests . functions import is_guid


class InfoClass:
    request_class = None
    entry_class = InfoEntry
    info_list = []
    name_field = ''
    names = []
    name_lookup = {}
    id_field = ''
    ids = []
    id_lookup = {}

    def __init__(self, api_session):
        self.request = self.request_class(api_session)
        self.load_info()

    def load_info(self):
        for entry in self.request.response_dict:
            self.add_entry(entry)

    def add_entry(self, entry):
        new_entry = self.entry_class(
            entry[self.id_field], entry[self.name_field])
        self.info_list.append(new_entry)
        new_entry_index = self.info_list.index(new_entry)
        self.ids.append(entry[self.id_field])
        self.id_lookup[entry[self.id_field]] = new_entry_index
        self.names.append(entry[self.name_field])
        self.name_lookup[entry[self.name_field]] = new_entry_index

    def __getitem__(self, key):
        if key in self.id_lookup:
            return self.info_list[self.id_lookup[key]]
        elif key in self.names:
            return self.info_list[self.name_lookup[key]]
        else:
            return self.info_list[key]
