from . channels import Channels
from . shipping_methods import ShippingMethods
from . postage_services import PostageServices
from . package_groups import PackageGroups
from . categories import Categories
from . locations import Locations
from .. pylinnworks import PyLinnworks


class Settings(PyLinnworks):
    channels = None
    shipping_methods = None
    postage_services = None
    package_groups = None
    categories = None
    locations = None

    def __init__(self):
        self.channels = Channels(self)
        self.shipping_methods = ShippingMethods(self)
        self.postage_services = PostageServices(self)
        self.package_groups = PackageGroups(self)
        self.categories = Categories(self)
        self.locations = Locations(self)

    @classmethod
    def get_categories(cls):
        if cls.categories is None:
            cls.categories = Categories(cls)
        return cls.categories

    @classmethod
    def get_category_by_ID(cls, category_id):
        categories = cls.get_categories()
        return categories.get_by_ID(category_id)

    @classmethod
    def get_category_by_name(cls, name):
        categories = cls.get_categories()
        return categories.get_by_name(name)

    @classmethod
    def get_shipping_methods(cls):
        if cls.shipping_methods is None:
            cls.shipping_methods = ShippingMethods(cls)
        return cls.shipping_methods

    @classmethod
    def get_shipping_method_by_ID(cls, shipping_method_id):
        shipping_methods = cls.get_shipping_methods()
        return shipping_methods.get_by_ID(shipping_method_id)

    @classmethod
    def get_shipping_method_by_name(cls, name):
        shipping_methods = cls.get_shipping_methods()
        return shipping_methods.get_by_name(name)

    @classmethod
    def get_postage_services(cls):
        if cls.postage_services is None:
            cls.postage_services = PostageServices(cls)
        return cls.postage_services

    @classmethod
    def get_postage_service_by_ID(cls, postage_service_id):
        postage_services = cls.get_postage_services()
        return postage_services.get_by_ID(postage_service_id)

    @classmethod
    def get_postage_service_by_name(cls, name):
        postage_services = cls.get_postage_services()
        return postage_services.get_by_name(name)

    @classmethod
    def get_package_groups(cls):
        if cls.package_groups is None:
            cls.package_groups = PackageGroups(cls)
        return cls.package_groups

    @classmethod
    def get_package_group_by_ID(cls, package_group_id):
        package_groups = cls.get_package_groups()
        return package_groups.get_by_ID(package_group_id)

    @classmethod
    def get_package_group_by_name(cls, name):
        package_groups = cls.get_package_groups()
        return package_groups.get_by_name(name)

    @classmethod
    def get_locations(cls):
        if cls.locations is None:
            cls.locations = Locations(cls)
        return cls.locations

    @classmethod
    def get_location_by_ID(cls, location_id):
        locations = cls.get_locations()
        return locations.get_by_ID(location_id)

    @classmethod
    def get_location_by_name(cls, name):
        locations = cls.get_locations()
        return locations.get_by_name(name)
