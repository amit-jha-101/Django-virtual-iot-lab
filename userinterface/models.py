from django.db import models
import uuid
# Create your models here.
class CronData(models.Model):
    SensorName = models.CharField(max_length = 255, primary_key = True, null = False,default = uuid.uuid4)
    testTime = models.IntegerField()
    testStatus = models.CharField(max_length = 255, default = "off")

    def __str__(self):
        return "Sensor : "+str(self.SensorName)+"  testTime: "+ str(self.testTime)+" in min"
