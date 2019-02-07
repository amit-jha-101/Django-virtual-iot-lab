from django.shortcuts import render
import boto3
# Create your views here.
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .functions import API 
from .dashboard_funcs import Dashboard
from rest_framework.decorators import api_view
from rest_framework import status
import json
from decimal import Decimal
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from userinterface.views import dashboard



@api_view(['GET'])
def getThings(request):
        if request.method == 'GET':
            dash=Dashboard()
        
            return Response(dash.get_things())

@api_view(['GET'])
def makeTable(request, tableName = None):
        if request.method == 'GET':
            if tableName == None:
                return Response(status = status.HTTP_400_BAD_REQUEST)
            else:
                api = Dashboard()
                data = api.getTableData(tableName)
                if data == None:
                    return Response(status = status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(data)


@api_view(['POST'])
def createSensor(request):
        if request.method == 'POST':
            try:
                print(request.data)
                data = request.data
                api = API()
                print("create Sensor")
                
                if 'active' in data:
                    pass
                else:
                    data['active'] = 'off'
                print(str(data))
                #Get the rules Defined if any

                rules=dict()
                no_of_rules=0
                rule_types=""
                rule_values=""
                try:
                    rules[data["type"]]=data["value"]
                    no_of_rules+=1
                    rule_types+=data["type"]
                    rule_values+=data["values"]
                    rules[data["type1"]]=data["value1"]
                    no_of_rules+=1
                    rule_types+='$'+data["type1"]
                    rule_values+='$',data["values1"]
                    rules[data["type2"]]=data["value2"]
                    no_of_rules+=1
                    rule_types+='$'+data["type2"]
                    rule_values+='$'+data["values2"]
                except:
                    pass

                #Create Thing_____
                attr={
                         "attributes":{
                                 "Enviornment":data["env"],
                                 "Location":data["Loc"],
                                 "Model":data["model"],
                                 "RuleCount":str(no_of_rules),
                                 "RuleTypes":rule_types,
                                 "RuleValues":rule_values
                         }
                 }
                data['attr'] = str(attr)
                arn=api.createThing(data["SensorName"],data["SensorType"],attr,data)
                data['arn'] = arn

                # #Create Policy
                pname=api.createPolicy(data["SensorName"],arn)
                  
                #Create Keys and certificates for the thing:
                certi=api.create_certi()
        
                      
                #Attach the policy to certificate created
      
                api.attach_policy_and_thing_to_certi(pname, data["SensorName"],certi["certificateArn"])
                print("api.insertThingData(data)")
                api.insertThingData(data)
                #save certi
                api.add_data_to_file(data["SensorName"], data["SensorName"]+".private.key", certi["keyPair"]["PrivateKey"])
                api.add_data_to_file(data["SensorName"],data["SensorName"]+".cert.pem",certi["certificatePem"])
                
                # CreateLambdafn
               
                api.make_lamda_function(data["SensorName"],rules)
                lambda_arn=api.create_lambda_fuction(data["SensorName"])
                print("api.create_table(data)")
                api.create_table(data)
                # CreateRule
                api.create_rule(data["SensorName"]+"Rule", data["RuleDescription"],data["SensorName"], lambda_arn)
                print("api.create_cron(data)")
                api.create_cron(data)

                return Response(status=status.HTTP_201_CREATED)
            
            except Exception as e:
                print(str(e))
                return Response(status = status.HTTP_204_NO_CONTENT)

                
