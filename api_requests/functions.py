import re


def SKU_exists(api, sku):
    url = api.server + '/api/Stock/SKUExists'
    data = {'SKU': sku}
    response = api.request(url, data)
    response_json = response.json()
    return response_json


def get_new_SKU(api):
    """Return unsed product SKU."""
    url = api.server + '/api/Stock/GetNewSKU'
    response = api.request(url)
    response_json = response.json()
    return response_json


def is_guid(guid):
    regex = re.compile(('^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab]'
                        '[a-f0-9]{3}-?[a-f0-9]{12}\Z'), re.I)
    match = regex.match(guid)
    return bool(match)
