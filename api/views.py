from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .functions import API
from rest_framework.decorators import api_view
from rest_framework import status
import json
from decimal import Decimal
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from userinterface.models import CronData


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


@api_view(['GET'])
def dynamo(request):
    if request.method == 'GET':
        api = API()
        # newData = "[{\"city\": \"Id1\", \"timestamp\": \"201812180203356\"}, {\"city\": \"Id1\", \"timestamp\": \"20181218020338\"}]"
        newData = api.getData()
        return Response(newData)



@api_view(['POST'])
@parser_classes((JSONParser,))
def testData(request):
    if request.method == 'POST':
        api = API()
        data =  request.data
        
        flag = api.pushOnCloud(data)
        if flag == True:
                return Response(status=status.HTTP_201_CREATED)
        else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def makeTable(request, tableName = None):
        if request.method == 'GET':
                if tableName == None:
                        return Response(status = status.HTTP_400_BAD_REQUEST)
                else:
                        api = API()
                        data = api.getTableData(tableName)
                        if data == None:
                                return Response(status = status.HTTP_400_BAD_REQUEST)
                        else:
                                return Response(data)

@api_view(['POST'])
def createSensor(request):
        if request.method == 'POST':
                #print(request.data)
                data = request.data
                #print(data)
                api = API()
                boolean = api.createThing(data)
                api.createTable(data)
                api.createRule(data)
                if boolean == True:
                        return Response(status= status.HTTP_201_CREATED)
                else:
                        return Response(status = status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def getThings(request):
        api = API()
        data = api.getThings()
        return Response(data)

@api_view(['GET'])
def getThingType(request):
        api = API()
        data = api.getThingType()
        newData={}
        newData['title'] = "Thing type  pie-chart"
        lis = []
        #newData['datas'] = data
        for l in data['dataset']:
                x = {}
                x['label'] = l['sensor_type']
                x['y'] = l['total']
                lis.append(x)
        print(str(lis))
        newData['dataPoints'] = lis
        #print(str(newData))
        return Response(newData)     


@api_view(['POST'])
def toggleTest(request):
        if request.method == 'POST':
                data = request.data
                if data['status'] == 'on':
                        dat = CronData.objects.filter(SensorName = data['name'], testStatus = data['status']).first()
                        dat.status = 'off'
                        dat.save(update_fields=['status'])
                else:
                        dat = CronData.objects.filter(SensorName = data['name'], testStatus = data['status']).first()
                        dat.status = 'on'
                        dat.save(update_fields=['status'])
