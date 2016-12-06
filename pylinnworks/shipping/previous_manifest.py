class PreviousManifest:
    def __init__(self, api_session, manifest, data):
        self.api_session = api_session
        self.manifest = manifest
        self.account_id = data['AccountId']
        self.date = data['Date']
        self.external_manifest_id = data['ExternalManifestId']
        self.is_complete = data['IsComplete']
        self.is_error = data['IsError']
        self.manifest_id = data['ManifestId']
        self.number_consignments = data['NumConsignments']
        self.reference = data['Reference']
        self.vendor = data['Vendor']
        self.shipping_api_config_id = data['fkShippingAPIConfigId']
