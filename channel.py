"""Container for selling channel """

class Channel():
    def __init__(self, channel_data):
        self.source = channel_data['Source']
        self.sub_source = channel_data['SubSource']
        self.source_type = channel_data['SourceType']
