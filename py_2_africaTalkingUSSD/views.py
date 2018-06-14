from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def process_ussd(request):
    ## MENU
    MY_COPERATIVE = 1
    WAZOBIA_LOANS = 2
    JOIN_AGBETUNTU = 3
    REQUEST_A_CALL = 4

    ## SUB MENU
    # MY_COPERATIVE SUBMENU
    CHECK_BALANCE = 1*1
    REQUEST_LOAN = 1*2
    MAKE_DEPOSIT = 1*3
    # WAZOBIA SUBMENU
    REGISTER = 2*1
    REQUEST_LOAN = 2*2
    MAKE_DEPOSIT = 2*3
    REQUEST_LOAN = 2*4
    REQUEST_A_CALL = 2*5

    if request.POST:
        
        import pdb; pdb.set_trace()
    return HttpResponse('Hello Africa Talking, It Peter Here!')
    # import pdb; pdb.set_trace()