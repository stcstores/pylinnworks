from pylinnworks.api_requests.inventory.add_inventory_item \
    import AddInventoryItem


class UpdateInventoryItem(AddInventoryItem):
    url_extension = '/api/Inventory/UpdateInventoryItem'
