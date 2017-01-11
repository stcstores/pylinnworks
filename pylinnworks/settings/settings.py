from . channels import Channels
from . shipping_methods import ShippingMethods
from . postage_services import PostageServices
from . package_groups import PackageGroups
from . categories import Categories
from . locations import Locations
from .. pylinnworks import PyLinnworks


class Settings(PyLinnworks):
    def __init__(self):
        self.channels = Channels(self)
        self.shipping_methods = ShippingMethods(self)
        self.postage_services = PostageServices(self)
        self.package_groups = PackageGroups(self)
        self.categories = Categories(self)
        self.locations = Locations(self)
