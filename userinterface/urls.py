from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create_sensor', views.create_sensor, name='create'),
    path('view_things', views.view_things, name='viewthings'),
    path('ctest/<slug:tableName>', views.tst, name='test'),
]
