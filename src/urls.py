app_name="src"
from django.contrib import admin
from django.urls import path 
from .views import *

urlpatterns = [
    path('', home , name="home" ),
    path('get_weather_info/', get_weather_info , name="get_whether_info" ),
]
