from django.contrib import admin
from .models import Weather_data,SensorData,ThingRules
# Register your models here.

admin.site.register(Weather_data)
admin.site.register(SensorData)
admin.site.register(ThingRules)