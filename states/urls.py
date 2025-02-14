
from django.contrib import admin
from django.urls import path
from django.urls import include, path

from states.views import *

urlpatterns = [
    path('switch_light/',pressLight,name='switch_light'),
    path('switch_door/',switch_door,name='switch_door'),
    path('get_light_state/',getLightState,name="getLightState"),
    path('get_tv_state/',getTvState,name="getTvState"),
    path('get_fan_level/',getFanState,name="getFanState"),

    path('get_tv_state_name/',getTvStateName,name="getTvStateName"),


    path('get_door_state/',getDoorState,name="getLightState"),
    path('set_temperature/<str:temperature>/<str:humidity>',set_temperature,name="set_temperature"),
    path('get_temperature/',get_temperature,name="get_temperature"),
    path('get_mode_state/',get_mode_state,name="get_mode_state"),
    path('switch_mode/',switch_mode,name="switch_mode"),
    path('switch_tv_channel/',switch_tv_channel,name="switch_tv_channel"),
    path('switch_fan_level/',switch_fan_level,name="switch_fan_level"),

]