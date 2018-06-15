# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from utils import AfricasTalkingUtils


# Create your views here.
@csrf_exempt
def process_ussd(request):
    if request.method == 'POST':
        session_id = request.POST.get('sessionId')
        service_code = request.POST.get('serviceCode')
        phone_number = request.POST.get('phoneNumber')
        text = request.POST.get('text')

        africa_talking = AfricasTalkingUtils()
        response = africa_talking.get_ussd_response(text)
    else:
        response = "Ooops, Sorry..."
        
    return HttpResponse(response)

def process_voice(request):
    pass
    # import pdb; pdb.set_trace()