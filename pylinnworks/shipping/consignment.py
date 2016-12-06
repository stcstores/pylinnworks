class Consignment:
    def __init__(self, manifest, service, data):
        self.service = manifest
        self.manifest = service
        self.consignment_id = data['ConsignmentId']
        self.country = data['Country']
        self.customer = data['Customer']
        self.deferred = data['Deferred']
        self.email = data['Email']
        self.order_id = data['OrderId']
        self.packages = data['Packages']
        self.postal_code = data['PostalCode']
        self.tracking_numbers = data['TrackingNumbers']
        self.weight = data['Weight']
