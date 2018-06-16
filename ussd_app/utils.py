from AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException
from . import models

## CONSTANT
PRODUCT_NAME = 'wazobia'
CURRENCY = 'NGN'

## MENU
MY_COPERATIVE = '1'
WAZOBIA_LOANS = '2'
JOIN_AGBETUNTU = '3'
REQUEST_A_CALL = '4'

## SUB MENU
# MY_COPERATIVE SUBMENU
CHECK_BALANCE = '1*1'
REQUEST_LOAN = '2*4'
MAKE_DEPOSIT = '1*3'
# WAZOBIA SUBMENU
REGISTER = '2*1'
REPAY_LOAN = '2*2'
MAKE_DEPOSIT_2 = '2*3'
REQUEST_LOAN_2 = '1*2'
REQUEST_A_CALL_2 = '2*5'
PROCESS_DEPOSIT = "231"

# REGISTER SUBMENU
WELCOME_USER = '2*1*1'

class AfricasTalkingUtils:
    def __init__(self, **kwargs):
        #Specify your credentials
        self.username = "sandbox"
        self.apiKey   = "93c1f491be8e3480265075a1b207cefc7601c36e06d66cc1a178aba7df633832"
        self.phonenumber = kwargs.get('phoneNumber', [None])[0]
        self.caller_number = kwargs.get('callerNumber', [None])[0]
        self.is_active = kwargs.get('isActive', [None])[0]
        self.duration_in_seconds = kwargs.get('du=rationInSeconds', [None])[0]
        self.currency_code = kwargs.get('currencyCode', [None])[0]
        self.amount = kwargs.get('amount', [None])[0]
        self.session_id = kwargs.get('sessionId', [None])[0]
        self.service_code = kwargs.get('serviceCode', [None])[0]
        self.text = kwargs.get('text', [None])[0]

        print(kwargs)

        self.customer = models.Account.get_current_customer(self.phonenumber)
        #Create an instance of our awesome gateway class and pass your credentials
        self.gateway = AfricasTalkingGateway(self.username, self.apiKey)

    def bank_checkout(self, **kwargs):
        # receive fund from customer
        try:
            # Send the request to the gateway. If successful, we will respond with
            # a transactionId that you can then use to validate the transaction
            transactionId = self.gateway.bankPaymentCheckoutCharge(
                productName_  = PRODUCT_NAME,
                currencyCode_ = CURRENCY,
                amount_       = kwargs['amount'],
                narration_    = kwargs['narration'],
                bankAccount_  = {
                    'accountName'   : kwargs['account_name'],
                    'accountNumber' : kwargs['account_num'],
                    'bankCode'      : kwargs['bank_code']
                    },
                metadata_     = {
                    'Reason' : 'To Test The Gateways'
                    }
            )       
            return transactionId
        except AfricasTalkingGatewayException, e:
            print 'Encountered an error while sending: %s' % str(e)

    def validate_payment(self, **kwargs):
        try:
            # Initiate the request with the transacitonId that was returned
            # by the charge request. If there are no exceptions, that means
            # the transaction was completed successfully
            self.gateway.bankPaymentCheckoutValidation(
                transactionId_ = kwargs['trans_id'],
                otp_           = kwargs['otp']
                )
            return True
            
        except AfricasTalkingGatewayException, e:
            print 'Encountered an error while sending: %s' % str(e)
        
    def pay_customers(self, **kwargs):
        recipients = [dict(bankAccount=dict(accountName=x['account_name'],
                            accountNumber=x['account_num'],
                            bankCode=x['bank_code']),
                    currencyCode='NGN', amount=x['amount'], narration=x['narration'],
                    metadata=dict(referenceId=x['reference_id'],officeBranch=x['office_branch'])
        ) for x in kwargs['recipients_list']]
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
                    return True
                else:
                    print "errorMessage=%s;" % response['errorMessage']
        except AfricasTalkingGatewayException, e:
            print 'Encountered an error while sending: %s' % str(e)
        pass

    def handle_calls(self, **kwargs):
        duration     = self.duration_in_seconds
        try:
            if self.is_active == '1': #make the call when isActive is 1
                        
                caller_number = self.caller_number or self.phonenumber

                # Compose the response
                response  = '<?xml version="1.0" encoding="UTF-8"?>'
                response += '<Response>'
                response += '<Say>Thank you for calling Good bye!</Say>'
                response += '</Response>'
                return response
            else: 
                #       # Read in call details (duration, cost)+ This flag is set once the call is completed+
                #       # Note that the gateway does not expect a response in thie case
                currencyCode = self.currency_code
                amount       = self.amount
            # You can then store this information in the database for your records

        except:
            print 'exception',duration
            
    def get_ussd_response(self, **kwargs):
        # main menu
        if self.text == "":
            response = "CON WELCOME, What would you want to check. \n"
            response += "1. My Cooperative \n"
            response += "2. Wazobia Loans \n"
            response += "3. Join Agbetuntun \n"
            response += "4. Request a Call \n"
        elif self.text == MY_COPERATIVE:
            response = "CON What would you like to do in You Cooperative account. \n"
            response += "1. Check Balance \n"
            response += "2. Accept Loan \n"
            response += "3. Make Deposit \n"
        elif self.text == WAZOBIA_LOANS:
            response = "CON WELCOME to Wazobia Loans \n"
            response += "1. Register \n"
            response += "2. Repay Loan \n"
            response += "3. Make Deposit \n"
            response += "4. Request Loan \n"
            response += "5. Request a call \n"
        
        elif self.text.startswith(REQUEST_LOAN):
            # request a loan
            if self.customer:
                if len(self.text.split('*')) == 3:
                    amount=self.text.split('*')[2]
                    response = "END An Agent will process your request and get back to you by text, \n"
                    response += "Enjoy Yourself!"
                    models.Transaction.record(
                                account=self.customer,
                                type=models.Transaction.LOAN,
                                status=models.Transaction.PENDING,
                                amount=amount
                            )
                else:
                    response = "CON Please specify the amount for the loan: \n"
            else:
                response = "END You are not a registered user, please register and try again.\n"
                
        elif self.text.startswith(REQUEST_LOAN_2):
            if self.customer:
                if len(self.text.split('*')) == 3:
                    narration = 'Loan from Wazobia group'
                    access_code=self.text.split('*')[2]
                    trans = models.Transaction.check_loan_validity(
                                            access_code=access_code,
                                            phonenumber=self.phonenumber)
                    if trans:
                        recipients_list = [
                            dict(account_name=self.customer.account_name, account_num=self.customer.account_number, 
                            bank_code=self.customer.bank_code, amount=int(trans.amount), narration=narration, reference_id=access_code, office_branch='201'),
                        ]
                        pay_status = self.pay_customers(recipients_list=recipients_list)
                        if pay_status:
                            balance, loan = trans.received_loan()
                            response = "END Your Loan Deposit is being processed. You will receive it shortly. \n"
                            response += "Balance: {} \n".format(balance)
                            response += "Loan: {} \n".format(loan)
                            response += "Enjoy Yourself!"
                        else:
                            response = "END Your Request was not successful \n"
                            response += "Please try again later {} \n".format(balance)
                    else:
                        response = "END Your Access Code is invalid.\n"
                        response += "Please try again.\n"
                        
                else:
                    response = "CON Please enter your loan access code to accept the loan requested.\n"
            else:
                response = "END You are not a registered user, please register and try again.\n"
                    
        # sub menu
        elif self.text == CHECK_BALANCE :
            # return user balance
            if self.customer:
                response = "END Balance: {}\n".format(self.customer.balance)
                response += "Loan: {}\n".format(self.customer.balance)
            else:
                response = "END You are not a registered user, please register and try again.\n"
                
        elif self.text.startswith(MAKE_DEPOSIT) or self.text.startswith(MAKE_DEPOSIT_2):
            if self.customer:
                if len(self.text.split('*')) == 3:
                    amount=self.text.split('*')[2] 
                    if self.customer:
                        narration = 'Deposit by {}'.format(self.customer.phonenumber)
                        deposit = self.bank_checkout(
                                    amount=amount, 
                                    narration=narration,
                                    account_name=self.customer.account_name, 
                                    account_num=self.customer.account_number, 
                                    bank_code=self.customer.bank_code)
                        if deposit:
                            models.Transaction.record(
                                account=self.customer,
                                type=models.Transaction.DEPOSIT,
                                trans_id=deposit,
                                status=models.Transaction.PENDING,
                                amount=amount
                            )
                            response = "CON Please enter OTP sent to your phone,\n";
                        else:
                            response = "END Your Deposite was not successful, please try again"

                elif len(self.text.split('*')) == 4:
                    otp = self.text.split('*')[3]
                    amount = self.text.split('*')[2]
                    trans = self.customer.get_last_trans(
                                status=models.Transaction.PENDING)
                    validate = self.validate_payment(otp=otp, trans_id=trans.trans_id)
                    if validate:
                        balance, loan = trans.mark_as_paid(amount=amount)
                        response = "END Deposit was successful,\n"
                        response += "New Balance: {}\n".format(balance)
                        response += "Loan: {}".format(loan)
                    else:
                        response = "END Your Deposite was not successful, please try again"
                else:
                    response = "CON Please enter amount: "
            else:
                response = "END You are not a registered user, please register and try again.\n"

        elif self.text.startswith(REGISTER) or self.text.startswith(JOIN_AGBETUNTU):
            balance = '0.00'
            resp, check_status = models.Account.create_account(phonenumber=self.phonenumber, check_status=True)
            if check_status == False:
                balance = self.customer.balance
                response = "END {} \n".format(resp)
                response += "Balance: {} {}\n".format(CURRENCY, self.customer.balance)
                response += "Loan: {} {}\n".format(CURRENCY, self.customer.loan)
            else:
                if(len(self.text.split('*')) == 3) and self.text[0] == JOIN_AGBETUNTU:
                    sort_code = self.text.split('*')[1]
                    account_number = self.text.split('*')[2]
                    resp, check_status = models.Account.create_account(self.phonenumber, 
                        sort_code, account_number, check_status=False)
                    response = "END Welcome to Agbetuntu \n"
                    response += "{}\n".format(resp)
                    response += "Balance: 0.00\n".format(CURRENCY)
                    response += "Loan: 0.00\n".format(CURRENCY)
                elif(len(self.text.split('*')) == 2) and self.text[0] == REGISTER.split('*')[0]:
                    response += "Please enter your account number 1 \n"
                elif (len(self.text.split('*')) == 4) and self.text[0] == REGISTER.split('*')[0]:
                    sort_code = self.text.split('*')[2]
                    account_number = self.text.split('*')[3]
                    resp, check_status = models.Account.create_account(self.phonenumber, 
                        sort_code, account_number, check_status=False)
                    response = "END Welcome to Agbetuntu \n"
                    response += "{}\n".format(resp)
                    response += "Balance: 0.00\n".format(CURRENCY)
                    response += "Loan: 0.00\n".format(CURRENCY)
                else:
                    response = "Please enter your bank sort code \n"

        elif self.text == REQUEST_A_CALL or self.text == REQUEST_A_CALL_2:
            response = self.handle_calls()
        elif self.text == REPAY_LOAN:
            response = self.customer.settle_loan()
        else:
            response = "CON You selected a wrong option, please try again\n"
            response += "Your Last Input was {} \n".format(self.text)
        return response

    # def get_voice_response(self, **kwargs):
        
# ussd=AfricasTalkingUtils()
# ussd.handle_calls()
pass