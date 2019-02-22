from django.shortcuts import render
from django.http import HttpResponse
#from Virtual_IoT_Lab.celery import hello
import boto3
import requests
import json
# Create your views here.


def dashboard(request):
    return render(request, 'userinterface/dashboard.html',{"Heading":"Dashboard"})

def create_sensor(request):
    client = boto3.client('iot')
    res = client.list_thing_types()
    l = res.get('thingTypes')
    return render(request, 'userinterface/createdevice.html',{"types":l,"Heading":"Create Device"})


def view_things(request):
    response = requests.get('http://localhost:8000/api/get_things').json()
    #print(response)
    return render(request, 'userinterface/viewthings.html', {'data':response,"Heading":"View Things"})

 
 

def tst(request,tableName):
    client = boto3.client('iot')
    response = requests.get('http://localhost:8000/api/makeTable/'+tableName).json()
    #print(response['Items'])
    #print(type(response['Items']))
    response=json.loads(response['Items'])
    desc=client.describe_thing(thingName=tableName)
    d=(desc['attributes'])
    l1=d['RuleTypes'].split("#")
    try:
        l2=d['RuleValues'].split("#")
    except:
        l2=["-","-","-"]
    
    return render(request, 'userinterface/test.html',{'data':response,'r':l1,'v':l2})

