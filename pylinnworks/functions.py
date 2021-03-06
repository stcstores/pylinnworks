def get_new_SKU(api_session):
    """Return unsed product SKU."""
    from pylinnworks.api_requests.inventory.get_new_sku import GetNewSKU
    request = GetNewSKU(api_session)
    return request.sku


def is_guid(guid):
    import re
    regex = re.compile(('^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab]'
                        '[a-f0-9]{3}-?[a-f0-9]{12}\Z'), re.I)
    match = regex.match(guid)
    return bool(match)


def get_order_number(api_session, order_number):
    from pylinnworks.api_requests.orders.\
        get_open_order_id_by_order_or_reference_id import \
        GetOpenOrderIDByOrderOrReferenceID
    from pylinnworks.orders import OpenOrder
    request = GetOpenOrderIDByOrderOrReferenceID(api_session, order_number)
    if is_guid(request.response_dict):
        order_id = request.response_dict
        try:
            order = OpenOrder(api_session, load_order_id=order_id)
        except:
            order = None
        return order
    else:
        return None


def get_order_id(api_session, order_number):
    from pylinnworks.api_requests import GetOpenOrderIDByOrderOrReferenceID
    from pylinnworks.api_requests import SearchProcessedOrdersPaged
    open_order_request = \
        GetOpenOrderIDByOrderOrReferenceID(
            api_session, order_number)
    open_order_request.response.raise_for_status()
    if open_order_request.response.text == 'null':
        processed_order_request = \
            SearchProcessedOrdersPaged(
                api_session, order_number, date_type='ALLDATES',
                exact_match=True, search_field='nOrderId')
        if len(processed_order_request.response_dict['Data']) == 1:
            return processed_order_request.response_dict[
                'Data'][0]['pkOrderID']
        else:
            return None
    else:
        return open_order_request.response_dict
