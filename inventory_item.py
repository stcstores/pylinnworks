

class InventoryItem:

    def __init__(self, api, stock_id):
        self.api = api
        self.stock_id = stock_id
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
        self.tax_rate = None
        self.variation_group_name = None
        self.weight = None
        self.width = None
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
        
    def get_all_details(self):
        self.get_inventory_item_details()
        self.get_extended_properties()
        
    def get_inventory_item_details(self):
        self.inventory_item_request = self.api.get_inventory_item_by_id(
                self.stock_id)
        
        self.category_id = self.inventory_item_request['CategoryId']
        self.category = self.inventory.category_lookup[self.category_id]
        self.depth = self.inventory_item_request['Depth']
        self.height = self.inventory_item_request['Height']
        self.package_group_id = self.inventory_item_request['PackageGroupId']
        self.package_group = self.inventory.postage_group_lookup[
                self.package_group_id]
        self.postage_service_id = self.inventory_item_request['PostalServiceId']
        self.postal_service = self.inventory.postal_service_lookup[
                self.postage_service_id]
        self.tax_rate = self.inventory_item_request['TaxRate']
        self.variation_group_name = self.inventory_item_request[
                'VariationGroupName']
        self.weight = self.inventory_item_request['Weight']
        self.width = self.inventory_item_request['Width']
        
    def get_extended_properties(self):
        
        self.extended_properties_request = self.api.get_inventory_item_extended_properties(self.stock_id)
        
        #Linnworks API contains spelling error ProperyName
        
        for prop in self.extended_properties_request:
            if prop['ProperyName'] not in self.inventory.extended_properties:
                self.inventory.extended_properties.append(prop['ProperyName'])
            
        self.extended_properties = {}
        
        for property_name in self.inventory.extended_properties:
            self.extended_properties[property_name] = ''
        
        for prop in self.extended_properties_request:
            self.extended_properties[prop['ProperyName']] = prop['PropertyValue']