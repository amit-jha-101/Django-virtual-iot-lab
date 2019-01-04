from django.shortcuts import render
from django.http import HttpResponse
from Virtual_IoT_Lab.celery import hello

# Create your views here.


def dashboard(request):
  return render(request, 'userinterface/createdevice.html')

def tst(request):
  hello.apply_async(args=[],countdown=3)
  return HttpResponse("WOOOWW")

