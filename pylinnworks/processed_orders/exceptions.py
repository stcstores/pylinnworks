class SearchFieldNotFound(Exception):
    def __init__(self, search_term):
        super().__init__(
            self, "No search field found matching '{}'".format(search_term))
