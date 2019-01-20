import requests
import json
from datetime import datetime
import os
from .models import SensorData,ThingRules,Policy
from django.conf import settings
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from boto3.dynamodb.conditions import Key, Attr
import boto3
import random
import string
import pandas as pd
from django.db.models import Count
from django.core import serializers
from userinterface.models import CronData
class API:

#this function by defaults queries a table in dynamoDB and returns data array in json format
#Here City should represent the sensor name and the eq field must map to DATE somehow
    dataframe = None
    def getData(self):
        conn = boto3.resource('dynamodb')
        table = conn.Table('temp')
        response = table.query(
            KeyConditionExpression=Key('city').eq('Id1')
        )
        items = response['Items']
        payload = json.dumps(items)
        return payload

# this function publishes the data to the topic and also adds the data to dynamoDB 
    def amazon(self, data):
        conn = boto3.resource('dynamodb')
        table = conn.Table('Temp_sensor')
        key = ''.join(random.choice(string.ascii_uppercase + string.digits)
                      for _ in range(8))
        newData = {}
        newData['key'] = key
        newData['data'] = data
        myMQTTClient = AWSIoTMQTTClient("Temp_sensor")
        myMQTTClient.configureEndpoint(
            "a3afa41mc06g6e.iot.us-west-2.amazonaws.com", 8883)
        myMQTTClient.configureCredentials(os.path.join(settings.ROOT_PATH, 'root-CA.crt'), os.path.join(settings.ROOT_PATH, 'Temp_sensor.private.key'),
                                          os.path.join(settings.ROOT_PATH, 'Temp_sensor.cert.pem'))
        print('start connection')
        # Infinite offline Publish queueing
        myMQTTClient.configureOfflinePublishQueueing(-1)
        myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        myMQTTClient.configureConnectDisconnectTimeout(1000)  # 10 sec
        myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
        myMQTTClient.connect()
        print('connected')
        print(newData)
        myMQTTClient.publish("Temp_sensor/info", "connected", 0)
        payload = json.dumps(data)
        response = table.put_item(
            TableName='Temp_sensor',
            Item=newData
        )
        myMQTTClient.publish("Temp_sensor/data", payload, 0)
        if response == None:
            return False
        else:
            return True
    
 # For just publishing the data to the topic defined by the sensor name present in the data   
    def pushOnCloud(self,data):
        topic = data['sensor']+"/data"
        # data['key'] = ''.join(random.choice(string.ascii_uppercase + string.digits)
        #               for _ in range(8))
        myMQTTClient = AWSIoTMQTTClient(data['sensor'])
        myMQTTClient.configureEndpoint(
            "a3afa41mc06g6e.iot.us-west-2.amazonaws.com", 8883)
        myMQTTClient.configureCredentials(os.path.join(settings.ROOT_PATH, 'root-CA.crt'), os.path.join(settings.ROOT_PATH, 'Temp_sensor.private.key'),
                                          os.path.join(settings.ROOT_PATH, 'Temp_sensor.cert.pem'))
        print('start connection')
        # Infinite offline Publish queueing
        myMQTTClient.configureOfflinePublishQueueing(-1)
        myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        myMQTTClient.configureConnectDisconnectTimeout(1000)  # 10 sec
        myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
        myMQTTClient.connect()
        print('connected')
        print('Topic is ', topic)
        print(data)
        payload = json.dumps(data)
        response=myMQTTClient.publish(topic, payload, 0)
        print("payload = ",payload)
        print(response)
        if response == None:
            return False
        else:
            return True
    
    # for getting the data from DynamoDB table
    def getTableData(self,tableName):
        if tableName == None:
            return None
        else:
            client = boto3.resource('dynamodb')
            table = client.Table(tableName)
            response = table.scan()
            items = response["Items"]
            lists = []
            for item in items:
                lists.append(item['payload'])
            self.dataframe =pd.DataFrame.from_dict(lists,orient="columns")
            Json = {}
            Json["Items"] = self.dataframe.to_json(orient='records')
            return Json

    def getMaxTemp(self):
        return self.dataframe['temperature'].max()
    
    def getMinTemp(self):
        return self.dataframe['temperature'].min()
    
    def createTable(self, data):
        dynamodb = boto3.client('dynamodb')
        table = dynamodb.create_table(
            TableName=str(data['SensorName']),
            KeySchema=[
                {
                    'AttributeName':'SensorName',
                    'KeyType':'HASH'
                },
                {
                    'AttributeName':'TimeStamp',
                    'KeyType':'RANGE'

                }

            ],
            AttributeDefinitions = [
                {
                    'AttributeName':'SensorName',
                    'AttributeType':'S'
                },
                {
                    'AttributeName':'TimeStamp',
                    'AttributeType':'S'
                }
            ],
             ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }

        )
    
    def createThing(self,data):
        client = boto3.client('iot')
        response = client.create_thing(
            thingName = data["SensorName"] ,
            thingTypeName = data["SensorType"],
            attributePayload={
                'attributes':{
                    "SensingType":data["SensingType"],
                    "model":data["model"]
                },
                'merge':True
            }
        )
        certificate = client.create_keys_and_certificate(setAsActive=True)
        print(str(certificate))
        if response == None:
            return False
        else:
            a = SensorData(sensor_name=data['SensorName'], 
            sensor_type=data['SensorType'],
            sensor_attributes=str({"SensingType": data["SensingType"],
                "model": data["model"]
            }),
            certificate_arn = certificate['certificateArn'],
            certificate_id = certificate['certificateId'],
            certificate_pem = certificate[ 'certificatePem'],
            public_key = certificate['keyPair']['PublicKey'],
            private_key = certificate['keyPair']['PrivateKey'],
            status = data['active'],
            timestamp = str(datetime.now()),
            interval = str(data['interval'])
            )
            a.save()
            self.createPolicy(data["SensorName"],certificate['certificateId'])
            cron = CronData(
                SensorName=data['SensorName'],
                testTime = data['interval'],
                testStatus = data['active'],
                ruleName = data['RuleName'],
                ruleType = data['RuleType'],
                ruleValue = data['RuleValue']

            )
            cron.save()
            return True

    

    def createRule(self, data):
        """
        This Function is used to create rule on AWS IoT core thing,
        this function applies the rule to the data which is being published
        args**
        ruleData:
            type: Dictionary
            Contents: Name of rule, Description of rule,Sql statement, Acess Resource, flag for rule
        """
        client = boto3.client('iot')
        data['sql'] = "SELECT * FROM '"+data['SensorName']+"'"
        print(data)
        client.create_topic_rule(
            ruleName = data['RuleName'],
            topicRulePayload = {
                'sql':data['sql'],
                'description':data['RuleDescription'],
                'actions':[
                    {
                       'lambda':{
                           'functionArn':'arn:aws:lambda:us-west-2:605025463444:function:MyLamdaIoT'
                       } 
                    }
                ],
                'ruleDisabled': False
            }
        )
        resp = client.get_topic_rule(
            ruleName = data['RuleName']
        )
        
        client = boto3.client('lambda')
        client.add_permission(
            FunctionName = "MyLamdaIoT",
            StatementId = "event"+data['RuleName'],
            Action = "lambda:InvokeFunction",
            Principal =  "iot.amazonaws.com",
            SourceArn = resp['ruleArn']    
        )
       
        rule = ThingRules(rule_name = data['RuleName'], rule_sql = data['sql'],sensor_name = data['SensorName'])
        rule.save()
    
    def getThings(self):
        """
            Gets list of things from aws-iot-core
        """
        things = SensorData.objects.all().values('sensor_name','sensor_type','timestamp','status','interval') 
        # listed = response['things']
        # data = {}
        # data['count'] = len(listed)
        # data['data'] = listed
        #data['dataset'] = json.loads(serializers.serialize('json',SensorData.objects.all()))
        #print(str(data))
        dat = {}
        dat["count"] = len(things)
        dat["data"]  = list(things)
        return dat

    def getThingType(self):
        """

        """
        getCountType =  SensorData.objects.all().values('sensor_type').annotate(total=Count('sensor_type'))
        print(str(getCountType))
        #print(json.loads(getCountType))
        data = {
            'dataset':list(getCountType)
        }
        print(str(data))
        return data
    
    def createPolicy(self, sensor_name,arn):
        """

        """
        client = boto3.client('iot')
        document = {
           
            "Version": "2012-10-17",
            "Statement": [
                {
                "Effect": "Allow",
                "Action": "iot:Connect",
                "Resource": "*"
                },
                {
                "Effect": "Allow",
                "Action": "iot:Receive",
                "Resource": "*"
                },
                {
                "Effect": "Allow",
                "Action": "iot:Publish",
                "Resource": "*"
                },
                {
                "Effect": "Allow",
                "Action": "iot:Subscribe",
                "Resource": "*"
                }
            ]
             
        }
        print(str(json.dumps(document)))
        response = client.create_policy(
            policyName=sensor_name,
            policyDocument = str(json.dumps(document))

        )
        policy = Policy(
            sensor_name = sensor_name,
             policyName = response['policyName'],
             policyArn = response['policyArn'],
             policyDocument = response['policyDocument'],
             policyVersionId = response['policyVersionId']
            )
        policy.save()
        # client.attach_policy(
        #     policyName = sensor_name,
        #     target = 'arn:aws:iam::605025463444:policy/Iot'
        # )






    



   
    








