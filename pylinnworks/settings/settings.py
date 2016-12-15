from . channels import Channels
from . shipping_methods import ShippingMethods
from . postage_services import PostageServices
from . package_groups import PackageGroups
from . categories import Categories


class Settings:
    def __init__(self, api_session):
        self.api_session = api_session
        self.channels = Channels(self.api_session)
        self.shipping_methods = ShippingMethods(self.api_session)
        self.postage_services = PostageServices(self.api_session)
        self.package_groups = PackageGroups(self.api_session)
        self.categories = Categories(self.api_session)
