import json
import os
import sys

config_path = os.path.join(
    os.path.realpath(os.path.dirname(__file__)), 'config.json')
config = json.load(open(config_path, 'r'))
config['application_token'] = sys.argv[1]
json.dump(
    config, open(config_path, 'w'), indent=4, sort_keys=True)
print('Token updated')
