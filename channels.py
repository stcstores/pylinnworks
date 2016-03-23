from . info_class import InfoClass
from . info_entry import InfoEntry
from . api_requests . info . get_channels import GetChannels
from . channel import Channel


class Channels(InfoClass):
    request_class = GetChannels
    entry_class = Channel
    info_list = []

    def add_entry(self, entry):
        self.info_list.append(
            self.entry_class(
                entry['PkChannelId'],
                entry['SourceType'],
                entry['Source'],
                entry['SubSource']))

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.info_list[key]
        if isinstance(key, str):
            for entry in self.info_list:
                if entry.sub_source == key:
                    return entry
            raise ValueError
        raise KeyError
