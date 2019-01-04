from django.contrib import admin
from .models import Rule,Device,Type
# Register your models here.
admin.site.register(Rule)
admin.site.register(Device)
admin.site.register(Type)