import uuid
import json

class InventoryItem:

    def __init__(self, api, stock_id=None):
        self.api = api
        if stock_id != None:
            self.stock_id = stock_id
        else:
            self.get_stock_id()
        self.json = None
        self.inventory = None
        self.sku = None
        self.title = None
        self.purchase_price = None
        self.retail_price = None
        self.barcode = None
        self.category = None
        self.depth = None
        self.height = None
        self.package_group_id = None
        self.package_group = None
        self.postage_service_id = None
        self.postage_service = None
        self.tax_rate = ''
        self.variation_group_name = None
        self.weight = None
        self.width = None
        self.quantity = None
        self.extended_properties = {}
        
    def load_from_json(self, json, inventory):
        self.json = json
        self.inventory = inventory
        self.api = self.inventory.api
        self.sku = json['SKU']
        self.title = json['Title']
        self.stock_id = json['Id']
        self.purchase_price = json['PurchasePrice']
        self.retail_price = json['RetailPrice']
        self.barcode = json['Barcode']
        
    def get_stock_id(self):
        self.stock_id = str(uuid.uuid4())
        
    def get_sku(self):
        self.sku = self.api.get_new_sku()
        
    def get_all_details(self):
        self.get_inventory_item_details()
        self.get_extended_properties()
        
    def get_inventoryItem_dict(self):
        inventoryItem = {}
        inventoryItem['ItemNumber'] = str(self.sku)
        inventoryItem['ItemTitle'] = str(self.title)
        inventoryItem['BarcodeNumber'] = str(self.barcode)
        inventoryItem['PurchasePrice'] = str(self.purchase_price)
        inventoryItem['RetailPrice'] = str(self.retail_price)
        inventoryItem['Quantity'] = str(self.quantity)
        inventoryItem['TaxRate'] = str(self.tax_rate)
        inventoryItem['StockItemId'] = str(self.stock_id)
        return inventoryItem
        
    def create_item(self):
        for prop in (self.stock_id, self.sku, self.title):
            assert(prop != None)
            
        inventoryItem = self.get_inventoryItem_dict()
        
        request_url = self.api.server + '/api/Inventory/AddInventoryItem'
        data = {'inventoryItem': json.dumps(inventoryItem)}
        
        return self.api.request(request_url, data, False)
    