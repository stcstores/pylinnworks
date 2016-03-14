"""Requests package group information"""

from . request import Request


class GetPackageGroups(Request):
    url_extension = '/api/Inventory/GetPackageGroups'
    info = []

    def __init__(self, api):
        super().__init__(api)
        self.execute()

    def process_response(self, response):
        self.info = self.get_info()
        self.names = self.get_names()
        self.ids = self.get_ids()

    def get_info(self):
        """Return package group information as dict."""
        info = []
        for package_group in self.response.json():
            new_group = {}
            new_group['id'] = package_group['Value']
            new_group['name'] = package_group['Key']
            info.append(new_group)
        return info

    def get_names(self):
        """Return package group names as list."""
        package_group_names = []
        for package_group in self.info:
            package_group_names.append(package_group['name'])
        return package_group_names

    def get_ids(self):
        """Return package group IDs as list."""
        package_group_ids = []
        for package_group in self.info:
            package_group_ids.append(package_group['id'])
        return package_group_ids

    def id_lookup(self, package_group_name):
        """Get package group id for package_group_name"""
        for package_group in self.info:
            if package_group['name'] == package_group_name:
                return package_group['id']
        raise ValueError(package_group_name + " Not in Package Groups")

    def name_lookup(self, package_group_id):
        """Get package group name for package_group_id"""
        for package_group in self.info:
            if package_group['id'] == package_group_id:
                return package_group['name']
        raise ValueError(package_group_id + " Not in Package Groups")
