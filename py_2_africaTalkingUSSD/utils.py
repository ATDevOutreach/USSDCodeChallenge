from AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException

class AfricasTalkingUtils:
    def __init__(self):
        #Specify your credentials
        self.username = "sandbox"
        self.apiKey   = "93c1f491be8e3480265075a1b207cefc7601c36e06d66cc1a178aba7df633832"
        #Create an instance of our awesome gateway class and pass your credentials
        self.gateway = AfricasTalkingGateway(self.username, self.apiKey)

    def bank_checkout(self):
        try:
            # Send the request to the gateway. If successful, we will respond with
            # a transactionId that you can then use to validate the transaction
            transactionId = self.gateway.bankPaymentCheckoutCharge(
            productName_  = 'Airtime Distribution',
            currencyCode_ = 'NGN',
            amount_       = 100,
            narration_    = 'Airtime Purchase Request',
            bankAccount_  = {
                'accountName'   : 'Fela Kuti',
                'accountNumber' : '123456789',
                'bankCode'      : 234001
                },
            metadata_     = {
                'Reason' : 'To Test The Gateways'
                }
            )       
            print transactionId
        except AfricasTalkingGatewayException, e:
            print 'Encountered an error while sending: %s' % str(e)

    def ussd(self, service_code, session_id, phone_number, text):
        import pdb; pdb.set_trace()
        