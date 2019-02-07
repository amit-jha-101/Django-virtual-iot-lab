from django.urls import path
from . import views

urlpatterns = [
    path('temperature/',views.temperature, name="Temperature"),
    path('humidity/',views.humidity, name="Humidity"),
    path('smoke/',views.smoke, name="Smoke"),
    path('waterlevel/',views.waterlevel, name="WaterLevel"),
    path('gps/',views.gps, name="GPS")
]