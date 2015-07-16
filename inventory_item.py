

class InventoryItem:

    def __init__(self, json, inventory):
        self.json = json
        self.inventory = inventory
        self.api = self.inventory.api
        self.sku = json['SKU']
        self.title = json['Title']
        self.stock_id = json['Id']
        self.purchase_price = json['PurchasePrice']
        self.retail_price = json['RetailPrice']
        self.barcode = json['Barcode']
        
    def get_inventory_item_details(self):
        self.inventory_item_request = self.api.get_inventory_item_by_id(
                self.stock_id)
        
        self.category_id = self.inventory_item_request['CategoryId']
        self.depth = self.inventory_item_request['Depth']
        self.height = self.inventory_item_request['Height']
        self.package_group_id = self.inventory_item_request['PackageGroupId']
        self.postage_service_id = self.inventory_item_request['PostalServiceId']
        self.tax_rate = self.inventory_item_request['TaxRate']
        self.variation_group_name = self.inventory_item_request[
                'VariationGroupName']
        self.weight = self.inventory_item_request['Weight']
        self.width = self.inventory_item_request['Width']
        
    def get_extended_propterties(self):
        
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