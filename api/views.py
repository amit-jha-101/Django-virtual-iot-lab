from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .function import API
from rest_framework.decorators import api_view
from rest_framework import status
import json
from decimal import Decimal

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
def testData(request):
    if request.method == 'POST':
        api = API()
        data = request.body
        print(data)

        newData = json.loads(data)
        print(newData)
        newData['value1'] = str(newData['value1'])
        flag = api.pushOnCloud(newData)
        if flag == True:
                return Response(status=status.HTTP_201_CREATED)
        else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
