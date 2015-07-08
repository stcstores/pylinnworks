

class InventoryItem:

    def __init__(self, json):
        self.sku = json['SKU']
        self.title = json['Title']
        self.stock_id = json['Id']
        self.purchase_price = json['PurchasePrice']
        self.RetailPrice = json['RetailPrice']
        
