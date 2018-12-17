from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Device
from .forms import DeviceCreationForm,RuleCreationForm
from .function import Methods
import requests
import json
def home(request):
  context = {
    'sensors': Device.objects.all()
  }
  return render(request, 'devices/sensors.html',context)

def create_d(request):
  if request.method == "POST":
    form = DeviceCreationForm(request.POST)
    if form.is_valid():
      form.save()
      #username=form.cleaned_data.get('username')
      # messages.success(
      #     request, f'Your account has been created! You can now Login')
      return redirect('devices-home')

  else:
    form = DeviceCreationForm()
  return render(request, 'devices/create.html', {'form': form})

def edit_d(request):
  
  return render(request, 'devices/sensors.html')

def test(request):
  context = {
    'sensors': Device.objects.all(),
  }
  return render(request,'devices/test.html',context)

def create_r(request):
  if request.method == "POST":
    form = RuleCreationForm(request.POST)
    if form.is_valid():
      data = {}
      func = Methods()
      f = form.cleaned_data
      data['name'] = f.get('name')
      data['sensor'] = str(f.get('sensor'))
      data['ruleType'] = f.get('Rule_type')
      data['ruleValue'] = f.get('ruleValue')
      data['ruleDescription'] = f.get('ruleDescription')
      data['ruleField'] = f.get('rule_field')
      data['ruleFlag'] = f.get('ruleFlag')
      data['sql'] = func.computeSql(data)
      func.createRule(data)
      form.save()
      
      #username=form.cleaned_data.get('username')
      # messages.success(
      #     request, f'Your account has been created! You can now Login')
      return redirect('devices-home')

  else:
    form = RuleCreationForm()
  return render(request, 'devices/rule.html', {'form': form})

# def about(request):
#   return render(request, 'blog/about.html', {'title': 'About'})



