from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='devices-home'),
    path('create',views.create_d,name='create_d'),
    path('newRule', views.create_r, name='create_r'),
    path('test',views.test,name='test'),
    path('analysis',views.analyse,name='analysis')
]
