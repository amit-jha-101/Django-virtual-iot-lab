from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
import requests

# Create your views here.

@api_view(['GET'])
def temperature(request):
        if request.method == 'GET':
            r=requests.get("http://api.openweathermap.org/data/2.5/weather?appid=f6182a9874fa6e1a215f5a7489f8b3eb&q=Mumbai").json()
            data={}
            data["value"]=r['main']['temp']-273.15    
            return Response(data)

@api_view(['GET'])
def humidity(request):
        if request.method == 'GET':
            r=requests.get("http://api.openweathermap.org/data/2.5/weather?appid=f6182a9874fa6e1a215f5a7489f8b3eb&q=Mumbai").json()
            data={}
            data["value"]=r['main']['humidity']
            return Response(data)

@api_view(['GET'])
def smoke(request):
        if request.method == 'GET':
            r=requests.get("http://api.openweathermap.org/data/2.5/weather?appid=f6182a9874fa6e1a215f5a7489f8b3eb&q=Mumbai").json()
            data={}
            data["value"]=r['weather'][0]['icon']    
            return Response(data)

@api_view(['GET'])
def gps(request):
        if request.method == 'GET':
                
            return Response("YEAYYY")

@api_view(['GET'])
def waterlevel(request):
        if request.method == 'GET':
                
            return Response("YEAYYY")
