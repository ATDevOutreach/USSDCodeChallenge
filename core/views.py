from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from core.utils.ATutils import ATutils
# Create your views here.

@csrf_exempt
def handle_ussd(request):
    if request.method == "POST":
        print(dict(request.POST))
        api_instance = ATutils(**request.POST)
        response = api_instance.get_ussd_response()
        print(response)
        return HttpResponse(response)

    return HttpResponse(status=200)

@csrf_exempt
def handle_voice(request):
    if request.method == 'POST':
        api_instance = ATUtils(**request.POST)
        response = api_instance.handle_calls()
    else:
        response = 'Ooops, sorry... #wink'

    return HttpResponse(response, content_type='application/xml')