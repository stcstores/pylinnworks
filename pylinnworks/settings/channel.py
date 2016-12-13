"""Container for selling channel """


class Channel():
    def __init__(self, channel_id, source_type, source, sub_source):
        self.channel_id = channel_id
        self.source_type = source_type
        self.source = source
        self.sub_source = sub_source

    def __lt__(self, other):
        return self.channel_id < other.channel_id

    def __str__(self):
        return '{} {}'.format(self.source, self.sub_source)
