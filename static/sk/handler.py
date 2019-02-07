import json
import boto3
import time
import datetime

def handler(event, context):
	valid=True
	value=event['value']
	sent_time=event['ts']
	 event['timeStamp']:str(datetime.now())