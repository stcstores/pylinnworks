from linnapi.api_requests.request import Request


class UpdateInventoryItemExtendedProperties(Request):
    url_extension = '/api/Inventory/UpdateInventoryItemExtendedProperties'

    def __init__(self, api_session, extended_properties):
        self.extended_properties = extended_properties
        super().__init__(api_session)

    def test_request(self):
        for ex_prop in self.extended_properties:
            assert 'pkRowId' in ex_prop \
                'Extended Property must contain pkRowId'
            assert is_guid(ex_prop['pkRowId']) 'pkRowId must be valid GUID'
            assert 'ProperyName' in ex_prop \
                'Extended Property must contain ProperyName'
            assert 'PropertyValue' in ex_prop \
                'Extended Property must contain PropertyValue'
            assert 'PropertyType' in ex_prop \
                'Extended Property must contain PropertyType'

    def get_data(self):
        data = {self.extended_properties}
        return data

    def test_response(self, response):
        assert isinstance(response.json(), list), \
            "Error message recieved: " + response.text
        return super().test_response(response)
