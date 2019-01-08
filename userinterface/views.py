from django.shortcuts import render
from django.http import HttpResponse
from Virtual_IoT_Lab.celery import hello
import requests
import json
# Create your views here.


def dashboard(request):
  response = requests.get('http://localhost:8000/api/getThings').json()
  data = {}
  data['count'] = response['count']
  response = requests.get('http://localhost:8000/api/getThingType').json()
  data['dataPoints'] = response['dataPoints']
  data['listSize'] = len(response['dataPoints'])
  data['title'] = response['title']
  print(str(data))
  
  return render(request, 'userinterface/dashboard.html',{'data':data})

def createDevice(request):
  return render(request, 'userinterface/createdevice.html' )


def tst(request):
  hello.apply_async(args=[],countdown=3)
  return HttpResponse("WOOOWW")


