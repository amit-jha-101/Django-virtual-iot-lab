import requests
import json
from datetime import datetime
import os
from .models import SensorData,CronData
from django.conf import settings
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from boto3.dynamodb.conditions import Key, Attr
from django.contrib.staticfiles.storage import staticfiles_storage
import boto3
import random
import string
import pandas as pd
from zipfile import ZipFile
import boto3
from django.core.files import File
from django.core.files.storage import FileSystemStorage
class API:
    client = boto3.client('iot')
    
    def createThing(self,thingName,thingType,attribs,dope):
        response = self.client.create_thing(
            thingName=thingName, thingTypeName=thingType, attributePayload=attribs)
        
        dope['timestamp'] = str(datetime.now())
        dope['thingArn'] = response['thingArn']
        print(str(dope))
        print("in create Thing")
        print(response["thingArn"])
        print("out from thing")
        return response["thingArn"]

    def createPolicy(self,name,arn):
        topicarn = arn[:arn.rfind(':')]
        print("in create policy")
        topicarn = topicarn+":topic/"+name+"Topic"
        doc ='{"Version": "2012-10-17","Statement": [{"Effect":"Allow","Action":"iot:Connect","Resource": "'+arn+'"},{"Effect": "Allow","Action": "iot:Publish","Resource": "'+topicarn+'"}]}'
        
        response = self.client.create_policy(
            policyName=name+"-policy",
            policyDocument=doc
        )
        return response["policyName"]
        

        
    
        
    def create_certi(self):
        print("in create Certi")
        response = self.client.create_keys_and_certificate(setAsActive=True)
        return response
    
    def attach_policy_and_thing_to_certi(self,policy_name,thing_name,certi_arn):
        print("in attach policy")
        self.client.attach_policy(policyName=policy_name,target=certi_arn)
        self.client.attach_thing_principal(thingName=thing_name,principal=certi_arn)
        
    def add_data_to_file(self,thing_name,file_name,file_content):
        print("adding data")
        url = staticfiles_storage.path(thing_name)
        if((os.path.isdir(url))):
            pass
        else:
            os.mkdir(url)
            
        myfile=open(url+"//"+file_name,'w')
        myfile.write(file_content)
        myfile.close()
        
    def make_lamda_function(self,thing_name,rules):
        url = staticfiles_storage.path(thing_name)
        print("making Lamda function")
        if(os.path.isdir(url)):
            pass
        else:
            os.mkdir(url)
        myfile=open(url+"//handler.py",'w')
        #basic code
        myfile.write("import json\nfrom decimal import Decimal\nimport boto3\nimport time\nimport datetime\n\ndef handler(event, context):\n\tvalid=True\n\tvalue=event['value']")
        #rules
        code=""
        myfile.write("\n\tevent['timeStamp']=str(datetime.datetime.now())")
        myfile.write("\n\tevent['latency']=str(abs(event['time1']-time.time()))")
        myfile.write("\n\tevent['ts']=str(event['ts'])")
        myfile.write("\n\tevent['time1']=str(event['time1'])")
        print(rules)
        for t,v in rules.items():
            if t=="gt":
                code+="\n\tif(value>"+v+"):\n\t\tvalid=False"
            elif t=="lt":
                code+="\n\tif(value<"+v+"):\n\t\tvalid=False"
            elif t=="e":
                code+="\n\tif(value=="+v+"):\n\t\tvalid=False"
        
        myfile.write("\n#Rules will execute here")
        myfile.write(code)
        #Action part
        #x = Sensor Name\n\t\ttable.put_item(Item= {'timestamp':str(datetime.datetime.now()),'value':  value,'valid':False})\n\t\tmessage = 'Value Alert ' + value+' for sensor "+thing_name+"'\n\t\tclient = boto3.client('sns')\n\t\tresponse = client.publish(TargetArn='arn:aws:sns:us-west-2:605025463444:notification',Message=json.dumps({'default': message}),MessageStructure='json' )
        myfile.write("\n\n\tif(valid):\n\t\tclient = boto3.resource('dynamodb')\n\t\ttable = client.Table('"+thing_name+"') #Sensor Name\n\t\ttable.put_item(Item= {'SensorName':'"+thing_name+"','timeStamp': str(datetime.datetime.now()),'value': event,'valid':True})\n\n\telse:\n\t\tclient = boto3.client('sns')\n\t\tresponse = client.publish(TopicArn = \'arn:aws:sns:us-west-2:605025463444:amit\',Message = str(event))")
        myfile.close()
        
    def create_lambda_fuction(self,thing_name):
        client = boto3.client('lambda')
        print("creaating Lamda Function")
        url = staticfiles_storage.path(thing_name)
        with ZipFile(url+"//handler.zip", "w") as newzip:
            newzip.write(url+"//handler.py","handler.py")
  
        encoded=None
        with open(url+"//handler.zip", 'rb') as f:
            encoded = f.read()
            
        response = client.create_function(
        FunctionName=thing_name+'-lambda',
        Runtime='python3.6',
        Role='arn:aws:iam::605025463444:role/lambda_basic_execution',
        Handler='handler.handler',
        Code={'ZipFile': encoded },
        Description='testing',
        )
        return response['FunctionArn']
    
    def create_rule(self,rule_name,rule_desc,thing_name,lambda_arn):
        print("creating Rule")
        self.client.create_topic_rule(
            ruleName=rule_name,
            topicRulePayload={
            'sql': "select * from '"+thing_name+"Topic'",
            'description': rule_desc,
            
            'actions': [
                {
                    'lambda': {
                    'functionArn': lambda_arn
                    }
                }
            ],
            'ruleDisabled': False,
            'errorAction': {
                'sns': {
                'targetArn': 'arn:aws:sns:us-west-2:605025463444:najiba',
                'roleArn': 'arn:aws:iam::605025463444:role/iotlab',
                'messageFormat': 'RAW'
                    },
                }
            }
            
        )
        resp = self.client.get_topic_rule(
            ruleName = rule_name
        )
        lamda = boto3.client('lambda')
        lamda.add_permission(
            FunctionName = thing_name+'-lambda',
            StatementId = "event-"+rule_name,
            Action = "lambda:InvokeFunction",
            Principal =  "iot.amazonaws.com",
            SourceArn = resp['ruleArn']
        )

    #Local DataBase operations
    def insertThingData(self,data):
        print("inserting thing Data")
        thing = SensorData(
            sensorName = data['SensorName'],
            sensorType = data['SensorType'],
            sensorAttributes= str(data['attr']),
            timestamp = str(datetime.now()),
            arn = data['arn']
        )

        thing.save()
        print("Inserted Thing Data ")

    def create_table(self,data):
        dynamodb = boto3.client('dynamodb')
        print("creating table")
        table = dynamodb.create_table(
            TableName=str(data['SensorName']),
            KeySchema=[
                {
                    'AttributeName':'SensorName',
                    'KeyType':'HASH'
                },
                {
                    'AttributeName':'timeStamp',
                    'KeyType':'RANGE'

                }

            ],
            AttributeDefinitions = [
                {
                    'AttributeName':'SensorName',
                    'AttributeType':'S'
                },
                {
                    'AttributeName':'timeStamp',
                    'AttributeType':'S'
                }
            ],
             ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }

        )       
        print("created Table")

        
    def create_cron(self,data):
        print("creating Cron")
        cron = CronData(
            SensorName = data['SensorName'],
            testTime = data['interval'],
            api = data['SensorType'],
            active = data['active']
        )
        cron.save()
        print("added cron")
    def add_perm_lamda(self,data):
        pass   
