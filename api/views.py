from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .function import API
from rest_framework.decorators import api_view
from rest_framework import status
import json
from decimal import Decimal
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser


@api_view(['POST'])
def postapi(request):
    if request.method == 'POST':
        api = API()
        data = request.body
        print(data)

        newData = json.loads(data)
        newData['Temperature'] = str(newData['Temperature'])
        flag = api.amazon(newData)
        if flag == True:
                return Response(status=status.HTTP_201_CREATED)
        else:
                return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@parser_classes((JSONParser,))
def testData(request):
    if request.method == 'POST':
        api = API()
        data =  request.data
        print(data)
        print(type(data))
        flag = api.pushOnCloud(data)
        if flag == True:
                return Response(status=status.HTTP_201_CREATED)
        else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
