from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from .models import CronData
import json
from django.core import serializers
import time
import os
from datetime import datetime
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute='*/2')),
    name="testInterval2",
    ignore_result=True
)
def testInterval2():
    """
        Schedules the task with schedule of 2 mins
    """
    data = json.loads(serializers.serialize('json',CronData.objects.all().filter(testTime = 2, testStatus = 'on')))
    f = open("demofile.txt", "a")
    f.write(str(data))
    print(str(data))
    f.close()
    logger.info(str(data))



def dataPush(data):
      #configure client params
    host = "a3afa41mc06g6e-ats.iot.us-west-2.amazonaws.com"
    arn = "arn:aws:iot:us-west-2:605025463444:thing/SensorA"
    rootCAPath = os.path.join(settings.ROOT_PATH, 'root-CA.crt')
    certificatePath = os.path.join(settings.ROOT_PATH, 'Temp_sensor.cert.pem')
    privateKeyPath = os.path.join(settings.ROOT_PATH, 'Temp_sensor.private.key')
    port = 443
    clientId = data['SensorName']
    topic = data['SensorName']

    myAWSIoTMQTTClient = AWSIoTMQTTClient(data['SensorName'])
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
    topic = data['SensorName']
    payload = json.dumps({
        "SensorName":data['SensorName'],
        "type": data['type'],
        "event_val": data['val'],
        "val": randVal()
    })
    myAWSIoTMQTTClient.publish(topic, payload, 0)

def randVal():
    pass

    
