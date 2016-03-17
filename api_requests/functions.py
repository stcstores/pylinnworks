import re


def SKU_exists(api_session, sku):
    url = api_session.server + '/api/Stock/SKUExists'
    data = {'SKU': sku}
    response = api_session.request(url, data)
    response_json = response.json()
    return response_json


def get_new_SKU(api_session):
    """Return unsed product SKU."""
    url = api_session.server + '/api/Stock/GetNewSKU'
    response = api_session.request(url)
    response_json = response.json()
    return response_json


def is_guid(guid):
    regex = re.compile(('^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab]'
                        '[a-f0-9]{3}-?[a-f0-9]{12}\Z'), re.I)
    match = regex.match(guid)
    return bool(match)


def get_stock_id_by_SKU(api_session, sku):
    from . inventory . inventory_view import InventoryView
    from . inventory . inventory_view_filter import InventoryViewFilter
    from . inventory . get_inventory_items import GetInventoryItems

    view = InventoryView()
    view.filters.append(InventoryViewFilter(
        field='String',
        value=sku,
        condition='Equals',
        filter_name='SKU',
        filter_name_exact=''
    ))
    response = GetInventoryItems(api_session, view=view)
    return response.response_dict['Items'][0]['Id']
