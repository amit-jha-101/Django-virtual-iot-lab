from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from api.models import CronData
import json
from django.conf import settings
from django.core import serializers
import time
import os
import boto3
from datetime import datetime
from random import randint
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute='*/5')),
    name="testInterval5",
    ignore_result=True
)
def testInterval2():
    """
        Schedules the task with schedule of 5 mins
    """
    data = CronData.objects.all().filter(testTime = 5, active = 'on').values()
    for i in data:
        dat = {}
        dat['SensorName'] = i['SensorName']
        
        
        dataPush(dat)
    
    logger.info(str(data))



def dataPush(data):
    client = boto3.client('iot-data')
    x = time.time()
    payload = json.dumps({
        "SensorName":data['SensorName'],
        "ts":str(datetime.now()),
        "value":randVal(),
        "ts":x,
        "time1":x
    })
    client.publish(
        topic = data['SensorName']+"Topic",
        qos = 0,
        payload = payload
    )
    

def randVal():
    print('hello')
    return randint(45,85)

    
