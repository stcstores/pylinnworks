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
