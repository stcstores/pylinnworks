import uuid
import json
import requests

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
        self.meta_data = ''
        self.extended_properties = _ExtendedProperties(self)
        
    def __str__(self):
        return str(self.sku) + ': ' + str(self.title)
        
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
        inventoryItem['MetaData'] = str(self.meta_data)
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
    
    def update_all(self):
        self.update_item()
        self.extended_properties.update()
    
    
    def load_extended_properties(self):
        self.extended_properties.load()
            
            
class _ExtendedProperties():
    
    
    def __init__(self, item):
        self.item = item
        self.extended_properties = []
        self.load()
        
        
    def load(self):
        response = self.item.api.get_inventory_item_extended_properties(self.item.stock_id)
        for _property in response:
            self.add(json=_property)
        
    def add(self, json):
        self.extended_properties.append(_ExtendedProperty(self.item, json=json))
        
    def create(self, name='', value='', property_type='Attribute'):
        prop = _ExtendedProperty(self.item)
        prop.name = name
        prop.value = value
        prop.type = property_type
        
        self.extended_properties.append(prop)
        
    def upload_new(self):
        new_properties = []
        for prop in self.extended_properties:
            if prop.on_server == False:
                new_properties.append(prop)
                
        if len(new_properties) > 0:
            item_arrays = []
            for prop in new_properties:
                item_arrays.append(prop.get_json())
                
            data = {'inventoryItemExtendedProperties' : json.dumps(item_arrays)}
            
            api = self.item.api
            url = api.server + '/api/Inventory/CreateInventoryItemExtendedProperties'
            response = requests.post(url, data=data, params={'token' : api.token})
            return response
    
    def update_existing(self):
        new_properties = []
        for prop in self.extended_properties:
            if prop.on_server == True:
                new_properties.append(prop)
                
        if len(new_properties) > 0:
            item_arrays = []
            for prop in new_properties:
                item_arrays.append(prop.get_json())
                
            data = {'inventoryItemExtendedProperties' : json.dumps(item_arrays)}
            
            api = self.item.api
            url = api.server + '/api/Inventory/UpdateInventoryItemExtendedProperties'
            response = requests.post(url, data=data, params={'token' : api.token})
            return response
    
        
    def update(self):
        self.upload_new()
        self.update_existing()
        
    def __getitem__(self, key):
        if type(key) == int:
            return self.extended_properties[key]
        elif type(key) == str:
            for prop in self.extended_properties:
                if prop.name == key:
                    return prop
    
    def __iter__(self):
        for prop in self.extended_properties:
            yield prop
    
    
    

class _ExtendedProperty():
    
    
    def __init__(self, item, json=None):
        self.item = item
        self.type = ''
        self.value = ''
        self.name = ''
        self.on_server = False
        
        if json != None:
            self.load_from_json(json)
            self.on_server = True
        else:
            self.guid = str(uuid.uuid4())
            self.on_server = False
            
    def load_from_json(self, json):
        self.type = json['PropertyType']
        self.value = json['PropertyValue']
        self.name = json['ProperyName']
        self.guid = json['pkRowId']
        
    def get_json(self):
        data = {}
        data['pkRowId'] = self.guid
        data['fkStockItemId'] = self.item.stock_id
        data['ProperyName'] = self.name
        data['PropertyValue'] = self.value
        data['PropertyType'] = self.type
        return data
        
    def update(self):
        api = self.item.api
        url = api.server + '/api/Inventory/UpdateInventoryItemExtendedProperties'
        data = {'inventoryItemExtendedProperties' : json.dumps([self.get_json()])}
        response = requests.post(url, data=data, params={'token' : api.token})
        return response
    
    def create(self):
        api = self.item.api
        url = api.server + '/api/Inventory/CreateInventoryItemExtendedProperties'
        data = {'inventoryItemExtendedProperties' : json.dumps([self.get_json()])}
        response = requests.post(url, data=data, params={'token' : api.token})
        return response