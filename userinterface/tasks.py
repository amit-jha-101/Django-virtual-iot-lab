from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from .models import CronData
import json
import boto3
from django.core import serializers
import time
import random
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
    task = CronData.objects.all().filter(testTime = 2, testStatus = 'on').values()
    for i in task:
        data = {}
        data['SensorName'] = i['SensorName']
        data['ruleName'] = i['ruleName']
        data['ruleType'] = i['ruleType']
        data['ruleValue'] = i['ruleValue']
        logger.info(str(data))
        dataPush(data)

    



def dataPush(data):
    client = boto3.client('iot-data')
    payload = json.dumps({
        "SensorName":data['SensorName'],
        "type": data['ruleType'],
        "event_val": data['ruleValue'],
        "val": randVal()
    })
    client.publish(
        topic = data['SensorName'],
        qos = 0,
        payload = payload
    )
    

def randVal():
    return random.randint(5,45)
    

    
