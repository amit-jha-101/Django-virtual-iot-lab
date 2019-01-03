from django.urls import path
from . import views

urlpatterns = [
    path('post/',views.postapi,name = " post-api"),
    path('pushData/',views.testData,name="pushData"),
    path('getData/',views.dynamo,name="getdata"),
    path('makeTable/<slug:tableName>',views.makeTable,name="makeTable"),
    path('create_thing/',views.createSensor, name="createSensor")

]