import requests
import json
from datetime import datetime
import os
from .models import SensorData,ThingRules
from django.conf import settings
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from boto3.dynamodb.conditions import Key, Attr
import boto3
import random
import string
import pandas as pd
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
            table = client.Table('temp')
            response = table.scan()
            items = response["Items"]
            lists = []
            for item in items:
                lists.append(item['payload'])
            self.dataframe =pd.DataFrame.from_dict(lists,orient="columns")
            Json = {}
            Json["Items"] = self.dataframe.to_json(orient='records')
            Json["Max"] = self.getMaxTemp()
            Json["Min"] = self.getMinTemp()
            Json["temperature"] = list(self.dataframe['temperature'])
            Json["timestamp"] = list(self.dataframe['timestamp'])
            return Json

    def getMaxTemp(self):
        return self.dataframe['temperature'].max()
    
    def getMinTemp(self):
        return self.dataframe['temperature'].min()
    
    def createTable(self, data):
        dynamodb = boto3.client('dynamodb')
        table = dynamodb.create_table(
            TableName=str(data['SensorName']+"Data"),
            KeySchema=[
                {
                    'AttributeName':'Sensor_id',
                    'KeyType':'HASH'
                },
                {
                    'AttributeName':'Sensor_name',
                    'KeyType':'RANGE'

                }

            ],
            AttributeDefinitions = [
                {
                    'AttributeName':'Sensor_id',
                    'AttributeType':'N'
                },
                {
                    'AttributeName':'Sensor_name',
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
                'attributes':data['attributes'],
                'merge':True
            }
        )

        if response == None:
            return False
        else:
            a = SensorData(sensor_name = data['SensorName'],sensor_type = data['SensorType'], sensor_attributes = data['attributes'])
            a.save()
            return True

    def errorTable(self,data):
        dynamodb = boto3.client('dynamodb')
        table2 = dynamodb.create_table(
            TableName=data['SensorName']+"Error",
            KeySchema=[
                {
                    'AttributeName':'Sensor_name',
                    'KeyType':'HASH'
                },
                {
                    'AttributeName':'Sensor_type',
                    'KeyType':'RANGE'

                }

            ],
            AttributeDefinitions = [
                {
                    'AttributeName':'Sensor_name',
                    'AttributeType':'S'
                },
                {
                    'AttributeName':'Sensor_type',
                    'AttributeType':'S'
                }
            ],
             ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }

        )
    

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
        data['sql'] = self.computeSql(data)
        arwAWS = 'arn:aws:iam::605025463444:role/DynamoDBaccess'
        tableName = data['SensorName']+"Data"
        print(data)
        client.create_topic_rule(
            ruleName = data['RuleName'],
            topicRulePayload = {
                'sql':data['sql'],
                'description':data['RuleDescription'],
                'actions':[
                    {
                        'dynamoDB': {
                            'tableName': tableName,
                            'roleArn': arwAWS,
                            'hashKeyField': 'Sensor_name',
                            'hashKeyValue': '${SensorName}',
                            'hashKeyType': 'STRING',
                            'rangeKeyField': 'Sensor_type',
                            'rangeKeyValue': '${SensorType}',
                            'rangeKeyType': 'STRING',
                            'payloadField': 'payload'
                        }
                    }
                ],
                'ruleDisabled': False
            }
        )
       
        rule = ThingRules(rule_name = data['RuleName'], rule_sql = data['sql'],sensor_name = data['SensorName'])
        rule.save()
    
    def computeSql(self, data):
        tableName = "'"+data['SensorName']+"Data'"
        condition = data['RuleField']
        val = str(data['RuleValue'])
        if data['RuleType'] == 'lb':
            condition = condition + " < " + val
        elif data['RuleType'] == 'ub':
            condition = condition + " > " + val
        else:
            condition = condition + " = " + val
        
        sql = "select * from "+tableName+" where "+condition

        print(sql)
        return sql




    



   
    








