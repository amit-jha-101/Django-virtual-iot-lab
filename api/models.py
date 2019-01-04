from django.db import models
from datetime import datetime
# Create your models here.
import uuid

class Weather_data(models.Model):
    Id=models.CharField(max_length=10,primary_key=True)
    time_stamp=models.DateTimeField(default=datetime.now())

    # City = models.CharField(max_length=255,blank=False)
    # Temperature = models.IntegerField()
    # id = models.AutoField(primary_key=True)
    # time_stamp = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return "{ ID : "+ self.Id + "\n Time Stamp : "+self.time_stamp+"\n }"
        

class SensorData(models.Model):
    sensor_name = models.CharField(max_length = 255,primary_key=True, default = uuid.uuid4)
    sensor_type = models.CharField(max_length = 255)
    sensor_attributes = models.TextField(blank=True, null=True)

    def __str__(self):
        return " sensor_name = "+str(self.sensor_name)+" sensor_type = "+str(self.sensor_type)




class ThingRules(models.Model):
    sensor_name = models.CharField(max_length = 255)
    rule_sql = models.CharField(max_length = 1000)
    rule_name = models.CharField(max_length = 255)

    def __str__(self):
        return " Rule Name : "+str(self.rule_name)+"  for sensor : "+ str(self.sensor_name)
