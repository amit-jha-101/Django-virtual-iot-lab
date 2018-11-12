from django.shortcuts import render,redirect
import boto3
from .forms import ThingCreate,PolicyCreate,TypeCreate
#import requests package for getting API responses
import requests
# import time module for getting the required pause in *seconds*
import time
# import datetime module for getting the timestamp
from datetime import datetime
import json

# Create your views here.
client = boto3.client('iot')
def thing(request):
    form = ThingCreate()
    if request.method == 'POST':
        form = ThingCreate(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            thingName = cd.get('Thing_Name')
            thingDesc = cd.get('Thing_Description')
            thingtype = cd.get('Thing_Type')
            print(thingName)
            print(thingDesc)
            print(thingtype)
            print(type(thingName))
            print(type(thingtype))
            name = {}
            name['thingName'] = thingName
            name['thingDesc'] = thingDesc
            name['thingtype'] = thingtype
            print(name)
            a = createThing(name)
            print(a)
            thingslist = client.list_things(
            )
            if a == True:
                return render(request,'dashboard/create.html',{'name':name,'list':thingslist})
            else:
                redirect('thing')

    return render(request,'dashboard/thing.html',{'form':form})

def createThing(d):
    thingname = str(d.get('thingName'))
    thingtype = str(d.get('thingtype'))
    client = boto3.client('iot')
  

    response = client.create_thing(thingName=thingname,thingTypeName=thingtype)
    if response == None:
        return False
    else:
        return True

def create(request):
    return render(request,'dashboard/create.html')

def drag(request):
    return render(request,'dashboard/drag-drop.html')

def policyfn(request):
    form=PolicyCreate()
    if request.method == 'POST':
        form = PolicyCreate(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            policyName = cd.get('Policy_Name')
            policyDocument = cd.get('Policy_Document')
            print(policyName)
            print(policyDocument)        
            response=client.create_policy(
                   policyName=policyName,
                   policyDocument=policyDocument
            )
           

        if response==None:
            return render(request,'dashboard/policy.html')
        else:
            redirect('create')

    return render(request,'dashboard/policy.html',{'form':form})

def thingfn(request):
    form=TypeCreate()
    if request.method == 'POST':
        form = TypeCreate(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            thingTypeName = cd.get('Thing_Type_Name')
            thingTypeDescription = cd.get('Thing_Type_Description')
            searchableAttributes=cd.get('Searchable_Attributes')
            attrList=searchableAttributes.split()
            print(thingTypeDescription)
            print(attrList)        
            response=client.create_thing_type(
                  thingTypeName=thingTypeName,
                  thingTypeProperties={
                      'thingTypeDescription':thingTypeDescription,
                      'searchableAttributes':attrList
                  }
            )
            print(response)

        if response==None:
            return render(request,'dashboard/thing.html')
        else:
            redirect('create')

    return render(request,'dashboard/thing.html',{'form':form})


def certifn(request):
    response = client.create_keys_and_certificate(
        setAsActive=True
    )
    print(response)

    if response == True:
        return render(request, 'dashboard/home.html',{'data':"Certificate Created Successfully"})
    else:
        redirect('home')

    return render(request, 'dashboard/home.html')


def home(request):
    return render(request, 'dashboard/home.html')

def temp(request):
    url1 = 'http://api.openweathermap.org/data/2.5/weather?appid=f6182a9874fa6e1a215f5a7489f8b3eb&q=Mumbai'
    count = 0
    l =[]
    while count < 5:
        data = {}
        json1 = requests.get(url1).json()
        count=count+1
        data['Mumbai']="{0:.2f}".format(float(json1['main']['temp'])-273.15)
        data['timestamp'] = str(datetime.now())
        data['count'] = count
        payload = json.dumps(data)
        print(payload)
        l.append(data)

    return render(request,'dashboard/temp.html',{"data":l})





    
