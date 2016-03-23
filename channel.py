"""Container for selling channel """


class Channel():
    def __init__(self, channel_id, source_type, source, sub_source):
        self.channel_id = channel_id
        self.source_type = source_type
        self.source = source
        self.sub_source = sub_source
