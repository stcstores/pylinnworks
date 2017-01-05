from .. pylinnworks import PyLinnworks
from . manifests import Manifests


class Shipping(PyLinnworks):

    @classmethod
    def get_manifest_consignments(cls):
        return Manifests(cls).get_consignments()

    @classmethod
    def get_manifests(cls):
        return Manifests(cls)
