"""Virtual_IoT_Lab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from dashboard import views as dash_views
from api import views as api_v
urlpatterns = [
    path('admin/', admin.site.urls),
    path('thing/', dash_views.thing,name="thing"),
    path('create/', dash_views.create,name="create"),
    path('drag/', dash_views.drag,name="drag"),
    path('policy/',dash_views.policyfn,name="policy"),
    path('type/',dash_views.thingfn,name='thing'),
    path('certi/',dash_views.certifn,name='certi'),
    path('home/', dash_views.home, name='home'),
    path('temp/',dash_views.temp,name='temp'),
    path('test1/', dash_views.test1, name='test1'),
    path('api/', include('api.urls')),
    path('devices/',include('devices.urls'))
]

