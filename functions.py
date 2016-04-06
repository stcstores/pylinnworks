def SKU_exists(api_session, sku):
    """Checks if sku has been used as a product SKU """
    from linnapi.api_requests.sku_exists import SKUExists
    request = SKUExists(api_session, sku)
    return request.response_dict


def get_new_SKU(api_session):
    """Return unsed product SKU."""
    from linnapi.api_requests.inventory.get_new_sku import GetNewSKU
    request = GetNewSKU(api_session)
    return request.sku


def is_guid(guid):
    import re
    regex = re.compile(('^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab]'
                        '[a-f0-9]{3}-?[a-f0-9]{12}\Z'), re.I)
    match = regex.match(guid)
    return bool(match)


def get_stock_id_by_SKU(api_session, sku):
    from linnapi.api_requests.inventory.inventory_view import InventoryView
    from linnapi.api_requests.inventory.inventory_view_filter \
        import InventoryViewFilter
    from linnapi.api_requests.inventory.get_inventory_items \
        import GetInventoryItems

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


def get_order_number(api_session, order_number):
    from linnapi.api_requests.orders.\
        get_open_order_id_by_order_or_reference_id import \
        GetOpenOrderIDByOrderOrReferenceID
    from linnapi.orders import OpenOrder
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


def get_inventory_item(api_session, stock_id=None, sku=None):
    from linnapi.inventory import InventoryItem
    if stock_id is None and sku is None or stock_id is not None and sku is not None:
        raise ValueError("Either stock_id or sku should be supplied")
    if sku is not None:
        stock_id = get_stock_id_by_SKU(api_session, sku)
    return InventoryItem(api_session, load_stock_id=stock_id)
