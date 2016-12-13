import pylinnworks.api_requests as api_requests
from . info_class import InfoClass
from . channel import Channel


class Channels(InfoClass):
    name = 'Channels'
    request_class = api_requests.GetChannels
    entry_class = Channel
    info_list = []
    sub_sources = []
    sub_source_lookup = {}

    def add_entry(self, entry):
        new_entry = self.entry_class(
                entry['PkChannelId'],
                entry['SourceType'],
                entry['Source'],
                entry['SubSource'])
        self.info_list.append(new_entry)
        self.info_list = sorted(self.info_list)
        new_entry_index = self.info_list.index(new_entry)
        self.sub_sources.append(entry['SubSource'])
        self.sub_source_lookup[entry['SubSource']] = new_entry_index

    def __getitem__(self, key):
        if key in self.sub_sources:
            return self.info_list[self.sub_source_lookup[key]]
        if isinstance(key, int):
            return self.info_list[key]
        if isinstance(key, str):
            for entry in self.info_list:
                if entry.sub_source == key:
                    return entry
            raise KeyError(key + " not in " + self.name)
        raise KeyError(self.name + " " + str(key) + " not found")
