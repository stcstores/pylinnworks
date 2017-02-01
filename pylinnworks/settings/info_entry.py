class InfoEntry:
    guid = None
    name = None

    def __init__(self, guid, name):
        self.guid = guid
        self.name = name

    def __repr__(self):
        return self.name
