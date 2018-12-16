from django.urls import path
from . import views

urlpatterns = [
    path('post',views.postapi,name = " post-api")

]