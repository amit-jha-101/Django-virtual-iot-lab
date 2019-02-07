import json
import boto3
import time
import datetime

def handler(event, context):
	valid=True
	value=event['value']
	sent_time=event['ts']
	event['timeStamp']:str(datetime.now())
	event['latency']:(float(event['time1'])-time.time())
#Rules will execute here
	if(value<0):
		valid=False

	if(valid):
		client = boto3.resource('dynamodb')
		table = client.Table('sww') #Sensor Name
		table.put_item(Item= {'SensorName':'sww','timeStamp': str(datetime.datetime.now()),'value': event,'valid':True})

	else:
		client = boto3.resource('sns')
		response = client.publish(TopicArn =  TopicArn = 'arn:aws:sns:us-west-2:605025463444:amit',Message = str(event)) 