from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('viewthings', views.viewthings, name='viewthings'),
    # path('ctest', views.tst, name='tst'),
    path('createSensor',views.createDevice,name='createDevice'),
    path('viewtable/<slug:tableName>',views.tableView, name="viewtable")
]
