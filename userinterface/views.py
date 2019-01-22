from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
from api.functions import API
# Create your views here.


def dashboard(request):
    response = requests.get('http://localhost:8000/api/getThings').json()
    data = {}
    data['count'] = response['count']
    data['ThingData'] = response['data']
    response = requests.get('http://localhost:8000/api/getThingType').json()
    data['dataPoints'] = response['dataPoints']
    data['listSize'] = len(response['dataPoints'])
    data['title'] = response['title']
    #print(str(data))

    return render(request, 'userinterface/dashboard.html',{'data':data})

def createDevice(request):
    return render(request, 'userinterface/createdevice.html' )


def viewthings(request):
    response = requests.get('http://localhost:8000/api/getThings').json()
    data = {}
    data['count'] = response['count']
    data['ThingData'] = response['data']
    response = requests.get('http://localhost:8000/api/getThingType').json()
    data['dataPoints'] = response['dataPoints']
    data['listSize'] = len(response['dataPoints'])
    data['title'] = response['title']
    print("___________________")
    print(data['ThingData'])
    return render(request, 'userinterface/viewthings.html', {'data': data['ThingData']})




def tst(request,tableName):
    response = requests.get('http://localhost:8000/api/makeTable/'+tableName).json()
    print(response['Items'])
    print(type(response['Items']))
    response=json.loads(response['Items'])
    return render(request, 'userinterface/test.html',{'data':response})

def tableView(request,tableName):
    obj = API()
    data = {}
    print(tableName)
    data['data'] = obj.getTableData(tableName)
    
    return render(request, 'userinterface/test.html',{'data':data['data']})

