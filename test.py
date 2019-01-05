
#import requests package for getting API responses

import requests
# import time module for getting the required pause in *seconds*
import time
# import datetime module for getting the timestamp
from datetime import datetime
import json
# install AWS Python SDK, you can install it as pip install boto3
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
# import json module for creating and handeling json


host = "a3afa41mc06g6e-ats.iot.us-west-2.amazonaws.com"
arn = "arn:aws:iot:us-west-2:605025463444:thing/SensorA"
rootCAPath = "root-CA.crt"
certificatePath = "SensorA.cert.pem"
privateKeyPath = "SensorA.private.key"
port = 443
clientId = 'SensorA'
topic = "pqrs"

#configure client params


myAWSIoTMQTTClient = AWSIoTMQTTClient("SensorA")
myAWSIoTMQTTClient.configureEndpoint(host, port)
myAWSIoTMQTTClient.configureCredentials(
rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
# Infinite offline Publish queueing
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
print("connected")
topic = 'SensorATopic'
payload = json.dumps({
    "value1": 90
})

print(myAWSIoTMQTTClient.publish(topic,payload,0))
