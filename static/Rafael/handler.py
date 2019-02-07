import json
import boto3
import datetime

def handler(event, context):
	valid=True
	value=event['value']
	sent_time=event['ts']
#Rules will execute here
	if(value>35):
		valid=False

	if(valid):
		client = boto3.resource('dynamodb')
		table = client.Table('Rafael') #Sensor Name
		table.put_item(Item= {'timestamp': str(datetime.datetime.now()),'value':  value,'valid':True})

	else:
		client = boto3.resource('dynamodb')
		table = client.Table('Rafael') #Sensor Name
		table.put_item(Item= {'timestamp':str(datetime.datetime.now()),'value':  value,'valid':False})
		message = 'Value Alert ' + value+' for sensor Rafael'
		client = boto3.client('sns')
		response = client.publish(TargetArn='arn:aws:sns:us-west-2:605025463444:notification',Message=json.dumps({'default': message}),MessageStructure='json' )