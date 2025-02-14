from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
modes = [
        ('Smart Mode', 'Smart Mode'),
        ('User Mode', 'User Mode'),
        ('Assisted Mode', 'Assisted Mode'),
 
    ]
# Create your models here.
class States(models.Model):
    room = models.CharField( max_length=50)
    light = models.BooleanField(blank=False,null=False)
    door = models.BooleanField(blank=False,null=False)
    pincode = models.CharField(max_length=4, validators=[MinLengthValidator(4), MaxLengthValidator(4)])
    temperature = models.FloatField()
    humidity =models.FloatField()
    mode = models.CharField(max_length=30, choices=modes)
    fanLevel = models.PositiveIntegerField(default=0)
    channelOn = models.PositiveIntegerField(default=0)
    channelName = models.CharField(max_length=30)

   