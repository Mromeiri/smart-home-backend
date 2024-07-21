# In admin.py

from django.contrib import admin
from .models import *

class LightDataSetAdmin(admin.ModelAdmin):
    list_display = ('timeOfDay', 'temperature', 'dayOfWeek', 'weatherConditions', 'motionDetection', 'LightIntensity','active')
    list_filter = ('dayOfWeek', 'weatherConditions', 'motionDetection')
    search_fields = ('weatherConditions', 'motionDetection')

admin.site.register(lightDataSet, LightDataSetAdmin)


class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ('day', 'time','month', 'outside_temperature', 'room_temperature', 'outside_humidity', 'room_humidity', 'outside_luminosity', 'motionDetection','fanLevel')
    list_filter = ('day', 'month', 'outside_temperature', 'room_temperature', 'outside_humidity', 'room_humidity', 'outside_luminosity', 'motionDetection','fanLevel')

admin.site.register(WeatherData, WeatherDataAdmin)

# Register your models here.
class TVDataSetAdmin(admin.ModelAdmin):
    list_display = ('timeOfDay', 'dayOfWeek', 'channelOn','motionDetection' )
    list_filter=("channelOn",)

admin.site.register(TVDataSet, TVDataSetAdmin)