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
        self.phonenumber = kwargs.get('phonenumber')
        self.callerNumber = kwargs.get('callerNumber')
        self.is_active = kwargs.get('isActive')
        self.duration_in_seconds = kwargs.get('durationInSeconds')
        self.currency_code = kwargs.get('currencyCode')
        self.amount = kwargs.get('amount')

        self.customer = models.Account.get_current_customer(kwargs.get('phonenumber'))
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
                        
                callerNumber = self.caller_number

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
            

    def ussd(self, **kwargs):
        pass
        # import pdb; pdb.set_trace()

    def get_ussd_response(self, **kwargs):
        # main menu
        if kwargs['text'] == "":
            response = "CON WELCOME, What would you want to check. \n"
            response += "1. My Cooperative \n"
            response += "2. Wazobia Loans \n"
        elif kwargs['text'] == MY_COPERATIVE:
            response = "CON What would you like to do in You Cooperative account. \n"
            response += "1. Check Balance \n"
            response += "2. Accept Loan \n"
            response += "3. Make Deposit \n"
        elif kwargs['text'] == WAZOBIA_LOANS:
            response = "CON WELCOME to Wazobia Loans \n"
            response += "1. Register \n"
            response += "2. Repay Loan \n"
            response += "3. Make Deposit \n"
            response += "4. Request Loan \n"
            response += "5. Request a call \n"
        elif kwargs['text'] == JOIN_AGBETUNTU:
            response = "CON Welcome to Agbetuntu"
        
        # elif kwargs['text'] == REQUEST_A_CALL or kwargs['text'] == REQUEST_A_CALL_2:
        #     # trigger call api
        #     response = "Your Request has been recorded, An agent will call soon! #CHEERS "
        elif kwargs['text'].startswith(REQUEST_LOAN):
            # request a loan
            if self.customer:
                if len(kwargs['text'].split('*')) == 3:
                    amount=kwargs['text'].split('*')[2]
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
                
        elif kwargs['text'].startswith(REQUEST_LOAN_2):
            if self.customer:
                if len(kwargs['text'].split('*')) == 3:
                    narration = 'Loan from Wazobia group'
                    access_code=kwargs['text'].split('*')[2]
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
        ## check balance Done
        elif kwargs['text'] == CHECK_BALANCE :
            # return user balance
            if self.customer:
                response = "CON Balance: {}\n".format(self.customer.balance)
                response = "Loan: {}\n".format(self.customer.balance)
            else:
                response = "END You are not a registered user, please register and try again.\n"
                

        ## make deposit Done
        elif kwargs['text'].startswith(MAKE_DEPOSIT):
            if self.customer:
                if len(kwargs['text'].split('*')) == 3:
                    amount=kwargs['text'].split('*')[2] 
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

                elif len(kwargs['text'].split('*')) == 4:
                    otp = kwargs['text'].split('*')[3]
                    amount = kwargs['text'].split('*')[2]
                    trans = self.customer.get_last_trans(
                                status=models.Transaction.PENDING)
                    validate = self.validate_payment(otp=otp, trans_id=trans.trans_id)
                    if validate:
                        balance, loan = trans.mark_as_paid(amount=amount)
                        response = "CON Deposit was successful,\n"
                        response += "New Balance: {}".format(balance)
                        response += "Loan: {}".format(loan)
                    else:
                        response = "END Your Deposite was not successful, please try again"
                else:
                    response = "CON Please enter amount: "
            else:
                response = "END You are not a registered user, please register and try again.\n"
                
        ## register user Done
        elif kwargs['text'] == REGISTER:
            resp = models.Account.create_account(phonenumber=self.phonenumber)
            response = "END \n".format(resp)
            response = "Balance: {} 0.00".format(CURRENCY)
        else:
            response = "CON You selected a wrong option, please try again\n"
            response += "Your Last Input was {} \n".format(kwargs['text'])
        return response

    def get_voice_response(self, **kwargs):
        response = self.handle_calls()
# ussd=AfricasTalkingUtils()
# ussd.handle_calls()
pass