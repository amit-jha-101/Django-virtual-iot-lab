from django.db import models
from datetime import datetime
# Create your models here.


class Weather_data(models.Model):
    City = models.CharField(max_length=255,blank=False)
    Temperature = models.IntegerField()
    id = models.AutoField(primary_key=True)
    time_stamp = models.DateTimeField(default=datetime.now())


    def __str__(self):
        return "{ City : "+ self.City + "\n temperature : "+ self.Temperature+" C\n"+" Time Stamp : "+self.time_stamp+"\n }"
