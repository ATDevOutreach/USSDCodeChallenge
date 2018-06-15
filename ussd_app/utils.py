from AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException

CURRENCY = 'NGN'

## MENU
MY_COPERATIVE = '1'
WAZOBIA_LOANS = '2'
JOIN_AGBETUNTU = '3'
REQUEST_A_CALL = '4'

## SUB MENU
# MY_COPERATIVE SUBMENU
CHECK_BALANCE = '1*1'
REQUEST_LOAN = '1*2'
MAKE_DEPOSIT = '1*3'
# WAZOBIA SUBMENU
REGISTER = '2*1'
REPAY_LOAN = '2*2'
MAKE_DEPOSIT = '2*3'
REQUEST_LOAN_2 = '2*4'
REQUEST_A_CALL_2 = '2*5'

# REGISTER SUBMENU
WELCOME_USER = '2*1*1'

class AfricasTalkingUtils:
    def __init__(self):
        #Specify your credentials
        self.username = "sandbox"
        self.apiKey   = "93c1f491be8e3480265075a1b207cefc7601c36e06d66cc1a178aba7df633832"
        #Create an instance of our awesome gateway class and pass your credentials
        self.gateway = AfricasTalkingGateway(self.username, self.apiKey)

    def bank_checkout(self):
        # receive fund from customer
        try:
            # Send the request to the gateway. If successful, we will respond with
            # a transactionId that you can then use to validate the transaction
            transactionId = self.gateway.bankPaymentCheckoutCharge(
                productName_  = 'wazobia',
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

    def validate_payment(self):
        try:
            # Initiate the request with the transacitonId that was returned
            # by the charge request. If there are no exceptions, that means
            # the transaction was completed successfully
            self.gateway.bankPaymentCheckoutValidation(
                transactionId_ = 'ATPid_5c8c64c82127820a0bb2bd5f34e419b0',
                otp_           = "1234"
                )
            print 'The transaction was completed successfully'
            
        except AfricasTalkingGatewayException, e:
            print 'Encountered an error while sending: %s' % str(e)
        
    def pay_customers(self):
        recipients_list = [
            dict(account_name='Peter Olayinka', account_num='0031116426', bank_code=234003, 
                amount=100, narration='May Salary', reference_id='1235', office_branch='201'),
            dict(account_name='Peter Olayinka', account_num='2074867972', bank_code=234004, 
                amount=100, narration='May Salary', reference_id='1235', office_branch='201')
            ]
        recipients = [dict(bankAccount=dict(accountName=x['account_name'],
                            accountNumber=x['account_num'],
                            bankCode=x['bank_code']),
                    currencyCode='NGN', amount=x['amount'], narration=x['narration'],
                    metadata=dict(referenceId=x['reference_id'],officeBranch=x['office_branch'])
        ) for x in recipients_list]
        try:
            responses = self.gateway.bankPaymentTransfer(
                productName_  = 'wazobia',
                recipients_   = recipients
                )
            for response in responses:
                print "accountNumber=%s;status=%s;" % (response['accountNumber'],
                                                        response['status'])
                if response['status'] == 'Queued':
                    print "transactionId=%s;transactionFee=%s;" % (response['transactionId'],
                                                                    response['transactionFee'])
                else:
                    print "errorMessage=%s;" % response['errorMessage']
        except AfricasTalkingGatewayException, e:
            print 'Encountered an error while sending: %s' % str(e)
        pass

    def handle_calls(self,**kwargs):
        try:
            if kwargs.get('is_active') == '1': #make the call when isActive is 1
                        
                callerNumber = kwargs.get('callerNumber')

                # Compose the response
                response  = '<?xml version="1.0" encoding="UTF-8"?>'
                response += '<Response>'
                response += '<Say>Thank you for calling Good bye!</Say>'
                response += '</Response>'
                return response
                # Print the response onto the page so that our gateway can read it
                # return HttpResponse(response, content_type='application/xml')
            else: 
                #       # Read in call details (duration, cost)+ This flag is set once the call is completed+
                #       # Note that the gateway does not expect a response in thie case
                duration     = kwargs.get('durationInSeconds')
                currencyCode = kwargs.get('currencyCode')
                amount       = kwargs.get('amount')
            # You can then store this information in the database for your records
        except:
            print 'exception',duration
            

    def ussd(self, service_code, session_id, phone_number, text):
        import pdb; pdb.set_trace()

    def get_ussd_response(self, text):
        # main menu
        if text == "":
            response = "CON WELCOME, What would you want to check. \n"
            response += "1. My Cooperative \n"
            response += "2. Wazobia Loans \n"
        elif text == MY_COPERATIVE:
            response = "CON What would you like to do in You Cooperative account. \n"
            response += "1. Check Balance \n"
            response += "2. Request Loan \n"
            response += "3. Make Deposit \n"
        elif text == WAZOBIA_LOANS:
            response = "CON WELCOME to Wazobia Loans \n"
            response += "1. Register \n"
            response += "2. Repay Loan \n"
            response += "3. Make Deposit \n"
            response += "4. Request Loan \n"
            response += "5. Request a call \n"
        elif text == JOIN_AGBETUNTU:
            response = "CON Welcome to Agbetuntu"
        
        # multiple options
        elif text == REQUEST_A_CALL or text == REQUEST_A_CALL_2:
            # trigger call api
            response = "Your Request has been recorded, An agent will call soon! #CHEERS "
        elif text == REQUEST_LOAN_2 or text == REQUEST_LOAN:
            # request a loan
            balance = 50
            response = "CON Loan Repaid, \n"
            response += "New Balance:", balance

        # sub menu
        elif text == CHECK_BALANCE :
            # return user balance
            balance = 200
            response = "CON Balance:", balance, "\n"
        elif text == MAKE_DEPOSIT:
            # deposit to account
            balance = 1000
            response = "CON Deposit was successful,\n"
            response += "New Balance:", balance

        elif text == REGISTER:
            # register user
            response = "CON Your Name"
        elif text == WELCOME_USER:
            # 
            response = "END Your phone number number has been successfully registerd\n"
            response = "Balance: {} 0.00\n".format(CURRENCY)
        else:
            response = "CON You selected a wrong option, please try again\n"
            response += "1. My Account \n"
            response += "2. My Phone Number \n"
            response += "Your Last Input was {} \n".format(text)
        return response

ussd=AfricasTalkingUtils()
ussd.handle_calls()
pass