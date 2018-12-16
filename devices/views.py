from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Device
from .forms import DeviceCreationForm,RuleCreationForm


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


def create_r(request):
  if request.method == "POST":
    form = RuleCreationForm(request.POST)
    if form.is_valid():
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



