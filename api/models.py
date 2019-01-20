from django.db import models
from datetime import datetime
# Create your models here.
import uuid



class SensorData(models.Model):
    sensor_name = models.CharField(max_length = 255,primary_key=True, default = uuid.uuid4)
    sensor_type = models.CharField(max_length = 255)
    sensor_attributes = models.TextField(blank=True, null=True)
    certificate_arn = models.TextField(blank = True, null =True)
    certificate_id = models.TextField(blank=True, null=True)
    certificate_pem = models.TextField(blank = True, null=True)
    public_key = models.TextField(blank = True, null= True)
    private_key = models.TextField(blank=True, null = True)
    timestamp = models.CharField(blank = True, null = True, max_length = 255)
    status = models.CharField(blank = True, null = True, max_length = 255)
    interval = models.CharField(blank = True, null = True, max_length = 255)
    

    def __str__(self):
        return " sensor_name = "+str(self.sensor_name)+" sensor_type = "+str(self.sensor_type)




class ThingRules(models.Model):
    sensor_name = models.CharField(max_length = 255)
    rule_sql = models.CharField(max_length = 1000)
    rule_name = models.CharField(max_length = 255)
    rule_value = models.IntegerField(default = 25)
    def __str__(self):
        return " Rule Name : "+str(self.rule_name)+"  for sensor : "+ str(self.sensor_name)

class Policy(models.Model):
    sensor_name = models.CharField(max_length = 255)
    policyName = models.CharField(max_length = 255)
    policyArn = models.CharField(max_length = 2048)
    policyDocument = models.TextField(blank=True, null = True)
    policyVersionId = models.TextField(blank=True, null = True)
    

    def __str__(self):
        return " Policy Name : "+self.policyName
 