class InfoEntry:
    guid = None
    name = None

    def __init__(self, guid, name):
        self.guid = guid
        self.name = name

    def __str__(self):
        return self.name
