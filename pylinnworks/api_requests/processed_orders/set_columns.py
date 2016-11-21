"""Sets columns for request to SearchProcessedOrdersPaged """

import json
from pylinnworks.api_requests.request import Request


class SetColumns(Request):
    url_extension = '/api/ProcessedOrders/SetColumns'

    def __init__(
            self, api_session, nOrderId=True, cEmailAddress=True,
            cFullName=True, fTotalCharge=True, Source=True, ReferenceNum=True,
            ChannelBuyerName=True, dReceivedDate=True, dProcessedOn=True,
            dPaidOn=True, timeDiff=True, PostalServiceName=True,
            fPostageCost=True, PostalTrackingNumber=True, cPostCode=True,
            cCountry=True, nStatus=True, SecondaryReference=True, Region=True,
            Town=True, Address3=True, Address2=True, Address1=True,
            AccountName=True, CountryTaxRate=True, PostageCostExTax=True,
            fTax=True, Subtotal=True, SubSource=True, Company=True,
            BuyerPhoneNumber=True, ExternalReference=True,
            PostalServiceCode=True, cCurrency=True):
        self.fields = {
            'nOrderId': nOrderId,
            'cEmailAddress': cEmailAddress,
            'cFullName': cFullName,
            'fTotalCharge': fTotalCharge,
            'Source': Source,
            'ReferenceNum': ReferenceNum,
            'ChannelBuyerName': ChannelBuyerName,
            'dReceivedDate': dReceivedDate,
            'dProcessedOn': dProcessedOn,
            'dPaidOn': dPaidOn,
            'timeDiff': timeDiff,
            'PostalServiceName': PostalServiceName,
            'fPostageCost': fPostageCost,
            'PostalTrackingNumber': PostalTrackingNumber,
            'cPostCode': cPostCode,
            'cCountry': cCountry,
            'nStatus': nStatus,
            'SecondaryReference': SecondaryReference,
            'Region': Region,
            'Town': Town,
            'Address3': Address3,
            'Address2': Address2,
            'Address1': Address1,
            'AccountName': AccountName,
            'CountryTaxRate': CountryTaxRate,
            'PostageCostExTax': PostageCostExTax,
            'fTax': fTax,
            'Subtotal': Subtotal,
            'SubSource': SubSource,
            'Company': Company,
            'BuyerPhoneNumber': BuyerPhoneNumber,
            'ExternalReference': ExternalReference,
            'PostalServiceCode': PostalServiceCode,
            'cCurrency': cCurrency}
        super().__init__(api_session)

    def get_data(self):
        data = {'columns': json.dumps(
            [field for field in self.fields if self.fields[field] is True])}
        self.data = data
        return data
