from django.contrib import admin
from django.urls import path
from django.urls import include, path

from smarthomeDataSets.views import *
# from states.views import *

urlpatterns = [
   
    path('admin/logout/', admin_logout, name='admin_logout'),
    path('index/', index, name='index'),
    path('accounts/register/', register, name='register'),
    path('insert/<str:temperature>/<str:motion_detection>/<str:light_intensity>/<str:active>/', insert_data, name='insert_data'),
    path('insert_tv/<str:motionDetection>/<str:channelOn>/', insert_tv, name='insert_tv'),
    path('insert_wether/<str:room_temperature>/<str:room_humidity>/<str:motionDetection>/<str:fanLevel>/', insert_wether, name='insert_wether'),

    path('download_excel/', download_excel, name='download_excel'),
    path('download_csv/', download_csv, name='download_csv'),
    path('download_csv_tv/', download_csv_tv, name='download_csv'),

    path('download_csv_wether/', download_csv_wether, name='download_csv'),

    path('prediction_light/', doPredLight, name='prediction_light'),
    path('prediction_fan/',predict_fan_level,name='predict_fan_level'),
    path('prediction_tv/', doPredTV, name='prediction_tv'),

    path('get_weather_json/',get_weather_json,name="get_weather_json")
   

]
