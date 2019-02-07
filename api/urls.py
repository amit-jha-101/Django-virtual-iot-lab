from django.urls import path
from . import views

urlpatterns = [
    path('create_thing/',views.createSensor, name="createSensor"),
    path('get_things/',views.getThings,name='getthings'),
    path('makeTable/<slug:tableName>',views.makeTable,name="makeTable"),

]