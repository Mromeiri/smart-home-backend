from django.db import models
from datetime import datetime
# Create your models here.
class lightDataSet(models.Model):
    timeOfDay = models.TimeField(auto_now=True, auto_now_add=False)
    temperature = models.FloatField(blank=False, null=False)
    dayOfWeek = models.IntegerField()  # Using IntegerField to store day of week
    weatherConditions = models.CharField(max_length=50)
    motionDetection = models.CharField(max_length=50)
    LightIntensity = models.FloatField(blank=False, null=False)
    active = models.BooleanField(blank=False, null=False)

    def save(self, *args, **kwargs):
        # Set the day of the week automatically before saving
        self.dayOfWeek = datetime.now().isoweekday()
        super(lightDataSet, self).save(*args, **kwargs)

import requests

class WeatherData(models.Model):
    time = models.TimeField(auto_now=True,)
    day = models.IntegerField(blank=True, null=True)
    month = models.CharField(max_length=20,blank=True, null=True)
    outside_temperature = models.DecimalField(max_digits=5, decimal_places=2,blank=True, null=True)  # Assuming temperature in Celsius
    room_temperature = models.DecimalField(max_digits=5, decimal_places=2)
    outside_humidity = models.DecimalField(max_digits=5, decimal_places=2,blank=True, null=True)  # Percentage value
    room_humidity = models.DecimalField(max_digits=5, decimal_places=2)
    outside_luminosity = models.DecimalField(max_digits=8, decimal_places=2,blank=True, null=True)  # Lux
    motionDetection = models.BooleanField(blank=False, null=False)
    fanLevel = models.PositiveIntegerField(default=0)
    def save(self, *args, **kwargs):
        # Automatically set the day and month when saving
        self.day = datetime.now().isoweekday()
        self.month = datetime.now().strftime('%B')
        latitude = 36.740509
        longitude = 3.115857
        api_key = '30d4741c779ba94c470ca1f63045390a'
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        print(data['main']['temp'])
        self.outside_temperature=data['main']['temp']
        self.outside_humidity=data['main']['humidity']
        self.outside_luminosity=data['visibility']
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} "


class TVDataSet(models.Model):
    timeOfDay = models.TimeField(auto_now=True, auto_now_add=False)
    
    dayOfWeek = models.IntegerField(blank=True, null=True)  # Using IntegerField to store day of week
    motionDetection = models.BooleanField(blank=False, null=False)
    channelOn = models.PositiveIntegerField(default=0)


    def save(self, *args, **kwargs):
        # Set the day of the week automatically before saving
        self.dayOfWeek = datetime.now().isoweekday()
        super(TVDataSet, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} "