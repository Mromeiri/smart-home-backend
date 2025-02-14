from django.contrib import admin

from states.models import States

# Register your models here.
class StatesAdmin(admin.ModelAdmin):
    list_display = ('id','room','light','door','temperature','humidity','pincode','mode','fanLevel','channelOn','channelName')
admin.site.register(States, StatesAdmin)