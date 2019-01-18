from django.contrib import admin
from .models import SensorData,ThingRules,Policy
# Register your models here.


admin.site.register(SensorData)
admin.site.register(ThingRules)
admin.site.register(Policy) 