import requests
import json
from datetime import datetime
import os
from .models import SensorData,CronData
from django.conf import settings
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from boto3.dynamodb.conditions import Key, Attr
from django.contrib.staticfiles.storage import staticfiles_storage
import boto3
import random
import string
import pandas as pd
from zipfile import ZipFile
import boto3
from django.core.files import File
from django.core.files.storage import FileSystemStorage
class Dashboard:
    client = boto3.client('iot')
    data_client=boto3.client('iot-data')
    
    def get_things(self):
        things=self.client.list_things()
        things=things["things"]
        n=len(things)
        stats=[]
        for i in range (0,n):
            stat=CronData.objects.filter(SensorName=things[i]["thingName"]).values('active').first()
            if(stat is None):
                stats.append("off")
            else:
                stats.append(stat["active"])
                
        print(stats) 
        d={}
        d["data1"]=things
        d["data2"]=stats 
        return(d)
    
    def getTableData(self,tableName):
        if tableName == None:
            return None
        else:
            client = boto3.resource('dynamodb')
            table = client.Table(tableName)
            print("15Feb"+tableName)
            response = table.scan()
            print(response)
            items = response["Items"]
            print(items)
            lists = []
            for item in items:
                lists.append(item['value'])
            self.dataframe =pd.DataFrame.from_dict(lists,orient="columns")
            Json = {}
            Json["Items"] = self.dataframe.to_json(orient='records')
            print(Json)
            return Json

    