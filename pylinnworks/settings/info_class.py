from . info_entry import InfoEntry


class InfoClass:
    name = ''
    request_class = None
    entry_class = InfoEntry
    name_field = ''
    id_field = ''

    def __init__(self, api_session):
        self.info_list = []
        self.ids = []
        self.names = []
        self.name_lookup = {}
        self.id_lookup = {}
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

    def get_by_ID(self, guid):
        try:
            return self.info_list[self.id_lookup[guid]]
        except:
            raise KeyError('{} found no GUID {}'.format(self.name, guid))

    def get_by_name(self, name):
        return self.info_list[self.name_lookup[name]]

    def __iter__(self):
        for item in self.info_list:
            yield item

    def __len__(self):
        return len(self.info_list)

    def __getitem__(self, key):
        if key in self.id_lookup:
            return self.info_list[self.id_lookup[key]]
        elif key in self.names:
            return self.info_list[self.name_lookup[key]]
        elif isinstance(key, int) and key >= 0 and key < len(self.info_list):
            return self.info_list[key]
        else:
            raise KeyError(str(key) + " not in " + str(self.name))
