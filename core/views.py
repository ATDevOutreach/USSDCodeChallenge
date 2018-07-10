from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
# Create your views here.

@csrf_exempt
def index(request):
    if request.method == "POST":
        from pprint import pprint
        pprint(request.POST)
    
    return HttpResponse(status=200)
