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
        africa_talking = AfricasTalkingUtils(**request.POST)
        response = africa_talking.get_ussd_response()
    else:
        response = "Ooops, Sorry... #wink"
        
    return HttpResponse(response)

@csrf_exempt
def process_voice(request):
    if request.method == 'POST':
        africa_talking = AfricasTalkingUtils(**request.POST)
        response = africa_talking.handle_calls()
    else:
        response = 'Ooops, sorry... #wink'

    return HttpResponse(response, content_type='application/xml')