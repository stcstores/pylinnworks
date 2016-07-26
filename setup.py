#! python3

import os
import shutil
import site
import json


class PackageSetup():
    def __init__(self):
        self.package_name = 'linnapi'
        self.source_dir = os.path.dirname(__file__)
        self.site_packages_dir = site.getsitepackages()[1]
        self.package = os.path.join(self.source_dir, self.package_name)
        self.package_dir = os.path.join(
            self.site_packages_dir, self.package_name)

    def install(self):
        print("Installing linnapi to " + self.package_dir)
        if os.path.exists(self.package_dir):
            shutil.rmtree(self.package_dir)
        shutil.copytree(self.package, self.package_dir)
        self.create_config()

    def create_config(self):
        self.config_file = os.path.join(self.package_dir, 'config.json')
        config = {
            'server': 'https://api.linnworks.net//',
            'application_id': 'da481ff0-7311-4d41-b42f-8507b269ae33',
            'application_secret': '2b96aca2-f15d-4e47-bfdd-24a5d07b4174',
            'application_token': ''}
        json.dump(
            config, open(self.config_file, 'w'), indent=4, sort_keys=True)

if __name__ == "__main__":
    installer = PackageSetup()
    installer.install()
