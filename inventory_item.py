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
        self.sku = ''
        self.title = ''
        self.purchase_price = 0
        self.retail_price = 0
        self.barcode = ''
        self.category_id = ''
        self.category = ''
        self.depth = ''
        self.height = ''
        self.package_group_id = ''
        self.package_group = ''
        self.postage_service_id = ''
        self.postage_service = ''
        self.tax_rate = 0
        self.variation_group_name = ''
        self.weight = 0
        self.width = 0
        self.quantity = 0
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
        
    def get_create_inventoryItem_dict(self):
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
        inventoryItem['VariationGroupName'] = str(self.variation_group_name)
        inventoryItem['MetaData'] = ''
        inventoryItem['CategoryId'] = str(self.category_id)
        inventoryItem['PackageGroupId'] = str(self.package_group_id)
        inventoryItem['PostalServiceId'] = str(self.postage_service_id)
        inventoryItem['Weight'] = str(self.weight)
        inventoryItem['Width'] = str(self.width)
        inventoryItem['Depth'] = str(self.depth)
        inventoryItem['Height'] = str(self.height)
        return inventoryItem
        
    def create_item(self):
        for prop in (self.stock_id, self.sku, self.title):
            assert(prop != None)
            
        inventoryItem = self.get_create_inventoryItem_dict()
        
        request_url = self.api.server + '/api/Inventory/AddInventoryItem'
        data = {'inventoryItem': json.dumps(inventoryItem)}
        
        return self.api.request(request_url, data, False)
    
    def update_item(self):
        for prop in (self.stock_id, self.sku, self.title):
            assert(prop != None)
            
        inventoryItem = self.get_inventoryItem_dict()
        
        request_url = self.api.server + '/api/Inventory/UpdateInventoryItem'
        data = {'inventoryItem': json.dumps(inventoryItem)}
        
        return self.api.request(request_url, data, False)
    
