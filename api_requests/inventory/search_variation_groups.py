"""Requests search of variation groups """

from .. request import Request


class SearchVariationGroups(Request):
    url_extension = '/api/Stock/SearchVariationGroups'
    search_types = ['VariationName', 'ParentSKU']
    count = 99999999
    page_number = 1

    def __init__(self, api_session, search_type, search_text=None,
                 page_number=None, count=None):
        if search_type is not None:
            self.search_type = search_type
        if search_text is not None:
            self.search_text = search_text
        if page_number is not None:
            self.page_number = page_number
        if count is not None:
            self.count = count
        super().__init__(api_session)

    def get_data(self):
        data = {
            'searchType': self.search_type,
            'searchText': self.search_text,
            'pageNumber': self.page_number,
            'entriesPerPage': self.count
        }
        return data

    def process_response(self, response):
        self.variation_groups = []
        for group in self.response_dict['Data']:
            new_group = {}
            new_group['parent_stock_id'] = group['pkVariationItemId']
            new_group['sku'] = group['VariationSKU']
            new_group['title'] = group['VariationGroupName']
            new_group['variation_group'] = True
            self.variation_groups.append(new_group)

    def test_response(self, response):
        assert isinstance(response.json(), dict), \
            "Error message recieved: " + response.text
        return super().test_response(response)
