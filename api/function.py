import requests
import json
from datetime import datetime
import os
from django.conf import settings
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import boto3
import random
import string

class API:
   
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

    



   
    








