class CustomerInfo:
    address = None
    company = None
    country = None
    country_id = None
    email = None
    name = None,
    phone = None
    post_code = None
    region = None,
    town = None
    billing_address = None
    channel_name = None

    def __init__(self, address=None, company=None, country=None,
                 country_id=None, email=None, name=None, phone=None,
                 post_code=None, region=None, town=None, billing_address=None,
                 channel_name=None):
        if address is not None:
            self.address = address
        if company is not None:
            self.company = company
        if country is not None:
            self.country = country
        if country_id is not None:
            self.country_id = country_id
        if email is not None:
            self.email = email
        if name is not None:
            self.name = name
        if phone is not None:
            self.phone = phone
        if post_code is not None:
            self.post_code = post_code
        if region is not None:
            self.region = region
        if town is not None:
            self.town = town
        if billing_address is not None:
            self.billing_address = billing_address
        if channel_name is not None:
            self.channel_name = channel_name
