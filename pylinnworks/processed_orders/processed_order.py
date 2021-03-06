"""ProcessedOrder class."""

from pylinnworks.api_requests import GetProcessedItemDetails
from . processed_order_item import ProcessedOrderItem


class ProcessedOrder:
    """Container for processed order."""

    def __init__(self, order_data):
        """Load data for order from SearchProcessedOrdersPaged request."""
        self.items = None
        self.account_name = order_data['AccountName']
        self.address1 = order_data['Address1']
        self.post_code = order_data['cPostCode']
        self.buyer_phone_number = order_data['BuyerPhoneNumber']
        self.full_name = order_data['cFullName']
        self.email_address = order_data['cEmailAddress']
        self.package_category = order_data['PackageCategory']
        self.billing_name = order_data['BillingName']
        self.channel_buyer_name = order_data['ChannelBuyerName']
        self.billing_address3 = order_data['BillingAddress3']
        self.paid_on = order_data['dPaidOn']
        self.address2 = order_data['Address2']
        self.region = order_data['Region']
        self.received_date = order_data['dReceivedDate']
        self.tax = order_data['fTax']
        self.time_diff = order_data['timeDiff']
        self.billing_address2 = order_data['BillingAddress2']
        self.shipping_address = order_data['cShippingAddress']
        self.address3 = order_data['Address3']
        self.country_tax_rate = order_data['CountryTaxRate']
        self.source = order_data['Source']
        self.status = order_data['nStatus']
        self.folder_collection = order_data['FolderCollection']
        self.currency = order_data['cCurrency']
        self.billing_country_name = order_data['BillingCountryName']
        self.billing_post_code = order_data['BillingPostCode']
        self.processed_on = order_data['dProcessedOn']
        self.billing_town = order_data['BillingTown']
        self.sub_source = order_data['SubSource']
        self.billing_address = order_data['cBillingAddress']
        self.total_charge = order_data['fTotalCharge']
        self.postage_cost = order_data['fPostageCost']
        self.billing_company = order_data['BillingCompany']
        self.billing_region = order_data['BillingRegion']
        self.postal_tracking_number = order_data['PostalTrackingNumber']
        self.postal_service_name = order_data['PostalServiceName']
        self.town = order_data['Town']
        self.billing_address1 = order_data['BillingAddress1']
        self.order_number = order_data['nOrderId']
        self.external_reference = order_data['ExternalReference']
        self.postage_cost_ex_tax = order_data['PostageCostExTax']
        self.hold_or_cancel = order_data['HoldOrCancel']
        self.total_weight = order_data['TotalWeight']
        self.package_title = order_data['PackageTitle']
        self.subtotal = order_data['Subtotal']
        self.secondary_reference = order_data['SecondaryReference']
        self.country = order_data['cCountry']
        self.postal_service_code = order_data['PostalServiceCode']
        self.total_discount = order_data['TotalDiscount']
        self.billing_phone_number = order_data['BillingPhoneNumber']
        self.company = order_data['Company']
        self.reference_num = order_data['ReferenceNum']
        self.vendor = order_data['Vendor']
        self.profit_margin = order_data['ProfitMargin']
        self.order_id = order_data['pkOrderID']
        self.item_weight = order_data['ItemWeight']

    def __repr__(self):
        return 'ProcessedOrder OrderID: {}'.format(self.order_id)

    def get_items(self):
        """Get list of items for this order."""
        request = GetProcessedItemDetails(self.order_id)
        items = [
            ProcessedOrderItem(item_data) for
            item_data in request.response_dict]
        self.items = items
        return items
