from django.db import models
from datetime import datetime
# Create your models here.
import uuid

class CronData(models.Model):
    SensorName=models.CharField(max_length = 255, primary_key = True,default = uuid.uuid4)
    testTime = models.IntegerField(default=10)
    api=models.CharField(max_length = 255,null = True)
    active=models.CharField(max_length = 255,null=True)
    def __str__(self):
        return "Sensor : "+str(self.SensorName)+"  (every "+ str(self.testTime)+" min)"
  

class SensorData(models.Model):
    sensorName = models.CharField(max_length = 255,primary_key=True, default = uuid.uuid4)
    sensorType = models.CharField(max_length = 255)
    sensorAttributes = models.TextField(blank=True, null=True)
    timestamp = models.CharField(blank = True, null = True, max_length = 255)
    arn = models.TextField(blank=True, null=True )
    def __str__(self):
        return " sensor_name = "+str(self.sensorName)+" sensor_type = "+str(self.sensorType)
