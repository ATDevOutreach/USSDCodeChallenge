from django.http import HttpResponse

def process_ussd_request(request):
    return HttpResponse('Hello Africa Talking, It Peter Here!')
    # import pdb; pdb.set_trace()