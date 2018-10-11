from django.shortcuts import render,redirect
import boto3
from .forms import ThingCreate
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

            if a == True:
                return render(request,'dashboard/create.html',{'name':name})
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