from django.contrib import admin
from api.models import CronData,SensorData
# Register your models here.
admin.site.register(CronData)
admin.site.register(SensorData)