import os
from ..models import WL_Account, Transaction

import africastalking

START_TEXT = ""
CURRENCY = "NGN"
PRODUCT_NAME = "wazobia_loans"

# MENU
MY_COOPERATIVE = "1"
WAZOBIA_LOANS = "2"
AGBETUNTUN = "3"
REQUEST_CALL = "4"

# SUBMENU

# MYCOOPERATIVE
MC_CHECK_BALANCE = "1*1"
MC_REQUEST_LOAN = "1*2"
MC_DEPOSIT = "1*3"

# WAZOBIA_LOANS
WL_REGISTER = "2*1"
WL_REPAY_LOAN = "2*2"
WL_DEPOSIT = "2*3"
WL_REQUEST_LOAN = "2*4"
WL_REQUEST_CALL = "2*5"

MENU_RESPONSES = {
    START_TEXT: """ 
                    CON Welcome, Select your service \r
                    1. My Cooperative \r
                    2. Wazobia Loans \r
                    3. Join Agbetuntun \r
                    4. Request a Call \r
                """,

    MY_COOPERATIVE: """
                        CON What service will you like to use in your Cooperative account. \r
                        1. Check Balance \r
                        2. Accept Loan \r
                        3. Make Deposit \r
                    """,

    WAZOBIA_LOANS: """
                        CON Welcome to Wazobia Loans, Kindly choose a service \r
                        1. Register \r
                        2. Repay Loan \r
                        3. Make Deposit \r
                        4. Request Loan \r
                        5. Request a call \r 
                   """,
    AGBETUNTUN: "END Coming Soon",

}

MENU_2_RESPONSES = {
    WL_REGISTER: """
                    CON Enter your account details in the form => Kanu James, 2034568902, 1 \r
                    1. FCMB Nigeria \r
                    2. Zenith Nigeria \r
                    3. Access Nigeria \r
                    4. Providus Nigeria \r
                    5. Sterling Nigeria \r
                 """,

    WL_DEPOSIT: """
                    CON You currently owe {}, How much will you like to deposit? \r
                """,

    WL_REQUEST_LOAN: """
                        CON How much loan do you need? \r
                     """,

    WL_REQUEST_CALL: """
                        END This feature will be available soon
                      """,
    
    MC_CHECK_BALANCE: """
                        END This feature will be available soon
                      """,

    MC_DEPOSIT: """
                    END This feature will be available soon
                """,

    MC_REQUEST_LOAN: """
                        END This feature will be available soon
                     """,                  
}


BANKS_LIST = {
    "1": {"name": "FCMB Nigeria", "code": 234001},
    "2":  {"name": "Zenith Nigeria", "code": 234002},
    "3":  {"name": "Access Nigeria", "code": 234003},
    "4":  {"name": "Providus Nigeria", "code": 234007},
    "5":  {"name": "Sterling Nigeria", "code": 234010},
}


class ATutils:
    def __init__(self, **kwargs):
        self.username = "sandbox"
        self.api_key = os.environ.get('API_KEY')
        self.phone_number = kwargs.get('phoneNumber', [None])[0]
        self.caller_number = kwargs.get('callerNumber', [None])[0]
        self.session_id = kwargs.get('sessionId', [None])[0]
        self.service_code = kwargs.get('serviceCode', [None])[0]
        self.text = kwargs.get('text', [""])[0]
        self.level = len(self.text.split('*'))
        
        #voice parameters
        self.is_active = kwargs.get('isActive', [None])[0]
        self.voice_duration = kwargs.get('durationInSeconds', [None])[0]
        

        self.customer = WL_Account.get_wl_account(
            phone_number=self.phone_number)

        africastalking.initialize(username=self.username, api_key=self.api_key)
        self.payment = africastalking.Payment
        self.voice = africastalking.Voice

    def handle_calls(self, **kwargs):
        duration = self.voice_duration
        try:
            if self.is_active == '1': #make the call when isActive is 1
                        
                caller_number = self.caller_number or self.phone_number

                # Compose the response
                response  = '<?xml version="1.0" encoding="UTF-8"?>'
                response += '<Response>'
                response += '<Say>Thanks for calling :) Good bye!</Say>'
                response += '</Response>'
                return response
            else: 
                currencyCode = CURRENCY
                return "END Call has been initiated, An agent will call soonest"
            
        except:
            print ('exception', duration)

    def register_wl_customer(self, *args, **kwargs):
        # get account name and number seperated by phone numbers
        account_details = self.text.split('*')[2].split(',')

        if len(account_details) != 3:
            return "END You inputted invalid values, Try again!"

        account_name, account_number, bank_short_code = account_details

        print(account_details)

        if bank_short_code.strip(" ") not in ["1", "2", "3", "4", "5"]:
            return "END You selected an invalid bank, Try again!"

        # check if number already exists in db
        customer, created = WL_Account.objects.get_or_create(
            phone_number=self.phone_number,
        )

        if created:
            customer.account_name = account_name
            customer.account_number = account_number.strip(" ")
            customer.bank_code = BANKS_LIST[bank_short_code.strip(" ")]["code"]
            customer.bank_name = BANKS_LIST[bank_short_code.strip(" ")]["name"]
            customer.save()
            return "END {}, your account has been successfully created :) !".format(account_name.split(' ')[0])

        return "END {}, your account already exists !!!".format(account_name.split(' ')[0])

    def handle_wl_deposit(self):
        deposit_amount = self.text.strip(WL_DEPOSIT + "*")
        narration = "Deposit from {} - {}".format(
            self.customer.account_name, self.customer.phone_number)

        account_details = {
            'accountNumber': self.customer.account_number,
            'bankCode': self.customer.bank_code,
            'accountName': self.customer.account_name
        }

        transaction_id = self.payment.bank_checkout(
            product_name=PRODUCT_NAME,
            currency_code=CURRENCY,
            amount=deposit_amount,
            narration=narration,
            bank_account=account_details
        )

        print("transaction id =>", transaction_id)
        if not transaction_id:
            return "END Your deposit was not successful"

        trans_instance = Transaction.objects.create(
            account=self.customer,
            type=Transaction.DEPOSIT,
            transaction_id=transaction_id,
            status=Transaction.PENDING,
            amount=deposit_amount
        )

        return "CON Please enter OTP sent to your phone,\r\n"

    def pay_loan(self):
        loan_amount = self.text.split('*')[2]
        recipients = [
            {"bankAccount": {
                "accountNumber": self.customer.account_number,
                "accountName": self.customer.account_name,
                "bankCode": self.customer.bank_code
            },
                "currencyCode": CURRENCY,
                "amount": loan_amount,
                "narration": "Loan to {} - {}".format(self.customer.account_name, self.customer.phone_number),
                "metadata": {}
            }
        ]
        result = self.payment.bank_transfer(
            product_name=PRODUCT_NAME, recipients=recipients)["entries"][0]

        print(result)

        if "errorMessage" in result.keys():
            return "END {}".format(result["errorMessage"])

        if result.status in ['InvalidRequest', 'NotSupported', 'Failed']:
            return "END An error occured when paying the loan, try again later"

        trans_instance = Transactions.objects.create(
            account=self.customer,
            transaction_id=result["transactionId"],
            status=Transaction.PENDING,
            type=Transaction.LOAN,
            amount=loan_amount,
            transaction_fee=result["transactionFee"]
        )

        #update debt balance
        self.customer.update_debt_balance(loan_amount)

        return "END Your request has been processed. you will recieve your loan shortly"

    def confirm_wl_deposit(self):
        otp = self.text.split('*')[3]
        transaction_amount = self.text.split('*')[2]
        last_transaction = self.customer.get_last_transaction(
            status=Transaction.PENDING)

        validate = self.payment.validate_bank_checkout(
            transaction_id=last_transaction.transaction_id, otp=otp)

        if validate:
            new_balance = last_transaction.mark_as_paid(
                amount=transaction_amount)
            response = """
                            END Your deposit of {} was successfuly completed,\r\n
                            New Balance=> {}\r\n
                       """.format(transaction_amount, new_balance)
        else:
            response = "END Your deposit was not successful, Try again later \r"

        return response

    def get_ussd_response(self, *args, **kwargs):
        # main menu
        print(self.text)

        # return menu reponses (Level 1)
        if self.level == 1:
            if self.text in MENU_RESPONSES.keys():
                response = MENU_RESPONSES[self.text]
                return response

            if self.text == REQUEST_CALL:
                response = self.handle_calls()
                return response

        # return sub menu responses (Level 2)
        if self.level == 2:
            if self.text in MENU_2_RESPONSES or self.text == WL_REPAY_LOAN:
               
                if self.text == WL_REGISTER:
                    if self.customer:
                        return "END {}, your account already exists !!!".format(self.customer.account_name.split(' ')[0])
               
                # only registered users can make use of service
                if self.text in [WL_DEPOSIT, WL_REPAY_LOAN, WL_REQUEST_LOAN]:
                    if not self.customer:
                        return "CON Sorry but you can't make use of this service till you register"

                    if self.text == WL_REPAY_LOAN:
                        response = self.customer.repay_debts()
                        return response

                    return MENU_2_RESPONSES[self.text].format(self.customer.debt)

                response = MENU_2_RESPONSES[self.text]
                return response

        if self.level == 3:
            # WAZOBIA LOANS
            if self.text.startswith(WL_REGISTER):
                response = self.register_wl_customer()
                return response

            if self.text.startswith(WL_DEPOSIT):
                response = self.handle_wl_deposit()
                return response

            if self.text.startswith(WL_REQUEST_LOAN):
                response = self.pay_loan()
                return response

        if self.level == 4:
            if self.text.startswith(WL_DEPOSIT):
                response = self.confirm_wl_deposit()
                return response

            if self.text.startswith(WL_REQUEST_LOAN):
                return

        return "END You entered an invalid option"
