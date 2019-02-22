import json
from decimal import Decimal
import boto3
import time
import datetime

def handler(event, context):
	valid=True
	value=event['value']
	event['timeStamp']=str(datetime.datetime.now())
	event['latency']=str(abs(event['time1']-time.time()))
	event['ts']=str(event['ts'])
	event['time1']=str(event['time1'])
#Rules will execute here
	if(value<0):
		valid=False
	if(value>100):
		valid=False

	if(valid):
		client = boto3.resource('dynamodb')
		table = client.Table('Lion') #Sensor Name
		table.put_item(Item= {'SensorName':'Lion','timeStamp': str(datetime.datetime.now()),'value': event,'valid':True})

	else:
		client = boto3.client('sns')
		response = client.publish(TopicArn = 'arn:aws:sns:us-west-2:605025463444:amit',Message = str(event))