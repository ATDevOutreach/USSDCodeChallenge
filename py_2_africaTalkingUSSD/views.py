from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from utils import AfricasTalkingUtils

@csrf_exempt
def process_ussd(request):
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

    if request.method == 'POST':
        session_id = request.POST.get('sessionId')
        service_code = request.POST.get('serviceCode')
        phone_number = request.POST.get('phoneNumber')
        text = request.POST.get('text')

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
            response = "Your Request has been recorded, An agent will call soon! #CHEERS "
        elif text == REQUEST_LOAN_2 or text == REQUEST_LOAN:
            balance = 50
            response = "CON Loan Repaid, \n"
            response += "New Balance:", balance

        # sub menu
        elif text == CHECK_BALANCE :
            balance = 200
            response = "CON Balance:", balance, "\n"
        elif text == MAKE_DEPOSIT:
            balance = 1000
            response = "CON Deposit was successful,\n"
            response += "New Balance:", balance

        elif text == REGISTER:
            response = "CON Your Name"
        else:
            response = "CON You selected a wrong option, please try again\n"
            response += "1. My Account \n"
            response += "2. My Phone Number \n"
        africa_talking = AfricasTalkingUtils()
    else:
        response = "Ooops, Sorry..."
        
    return HttpResponse(response)
    # import pdb; pdb.set_trace()