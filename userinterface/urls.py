from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # path('ctest', views.tst, name='tst'),
    path('createSensor',views.createDevice,name='createDevice')
]
