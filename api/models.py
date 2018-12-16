from django.db import models
from datetime import datetime
# Create your models here.


class Weather_data(models.Model):
    Id=models.CharField(max_length=10,primary_key=True)
    time_stamp=models.DateTimeField(default=datetime.now())

    # City = models.CharField(max_length=255,blank=False)
    # Temperature = models.IntegerField()
    # id = models.AutoField(primary_key=True)
    # time_stamp = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return "{ ID : "+ self.Id + "\n Time Stamp : "+self.time_stamp+"\n }"
        
