from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import json

from states.models import States

# Create your views here.
@csrf_exempt
def pressLight(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        newState = data.get('iss')
        
        
        room = States.objects.get(pk=1)
        if room:
            room.light = newState
            room.save()
            return JsonResponse({'status': 'success', 'message': 'Light switeched Successfully'})
        else :
            return JsonResponse({'status': 'error', 'message': 'Failed to switch light !!'})
    return JsonResponse({'message': 'Invalid request method'}, status=405)


@csrf_exempt
def switch_door(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        newState = data.get('state')
        pincode = data.get('pin_code')
        room = States.objects.get(pk=1)
        print(pincode)
        if pincode =="close":
            pincode = room.pincode
        
        
        
        if room:
            if room.pincode == pincode:
                room.door = newState
                room.save()
                return JsonResponse({'status': 'success', 'message': 'DOOR switeched Successfully'})
            else :
                return JsonResponse({'status': 'error', 'message': 'PINCODE INVALID'})
        else :
            return JsonResponse({'status': 'error', 'message': 'Failed to switch door !!'})
    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def switch_mode(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        newMode = data.get('mode_name')
        room = States.objects.get(pk=1)
        
        
        
        
        if room:
                room.mode = newMode
                room.save()
                return JsonResponse({'status': 'success', 'message': 'Mode switeched Successfully'})
           
        else :
            return JsonResponse({'status': 'error', 'message': 'Failed to switch mode !!'})
    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def switch_tv_channel(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        channel = data.get('channel')
        name = data.get('name')
        room = States.objects.get(pk=1)
        
        
        
        
        if room:
        
                room.channelOn = channel
                room.channelName = name
                room.save()
                return JsonResponse({'status': 'success', 'message': 'Channel switeched Successfully'})
            
        else :
            return JsonResponse({'status': 'error', 'message': 'Failed to switch Tv !!'})
    return JsonResponse({'message': 'Invalid request method'}, status=405)


@csrf_exempt
def switch_fan_level(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        fanLevel = data.get('fanLevel')
        room = States.objects.get(pk=1)
        
        
        
        
        if room:
        
                room.fanLevel = fanLevel
                room.save()
                return JsonResponse({'status': 'success', 'message': 'fanLevel switeched Successfully'})
            
        else :
            return JsonResponse({'status': 'error', 'message': 'Failed to switch fanLevel !!'})
    return JsonResponse({'message': 'Invalid request method'}, status=405)

def getLightState(request):
        room = States.objects.get(pk=1)
        if room:
            state = room.light
            
            return JsonResponse(state , safe = False)
        else :
            return JsonResponse({'status': 'error', 'message': 'Failed to get light !!'})
     
def getTvState(request):
        room = States.objects.get(pk=1)
        if room:
            state = room.channelOn
            
            return JsonResponse(state , safe = False)
        else :
            return JsonResponse({'status': 'error', 'message': 'Failed to get TV !!'})
def getFanState(request):
        room = States.objects.get(pk=1)
        if room:
            state = room.fanLevel
            
            return JsonResponse(state , safe = False)
        else :
            return JsonResponse({'status': 'error', 'message': 'Failed to get fanLevel !!'})
from django.http import JsonResponse, HttpResponse
from .models import States

def getTvStateName(request):
    try:
        room = States.objects.get(pk=1)
        state = room.channelName
        return HttpResponse(state, content_type="text/plain")
    except States.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Failed to get TV !!'}, status=400)

def getDoorState(request):
        room = States.objects.get(pk=1)
        if room:
            state = room.door
            
            return JsonResponse(state , safe = False)
        else :
            return JsonResponse({'status': 'error', 'message': 'Failed to get light !!'})   

@csrf_exempt
def set_temperature(request, temperature, humidity):
    if request.method == 'GET':
        try:
            room = States.objects.get(pk=1)
            if room:
                room.temperature = temperature
                room.humidity = humidity
                room.save()
                send_push_notification(temperature,humidity)
            return HttpResponse("Data inserted successfully!")
        except Exception as e:
            return HttpResponse(f"Error: {e}", status=400)
    else:
        return HttpResponse("Invalid method", status=405)

from django.http import JsonResponse

@csrf_exempt
def get_temperature(request):
    if request.method == 'GET':
        try:
            room = States.objects.get(pk=1)
            if room:
                data = {
                    "temp": room.temperature,
                    "humidity": room.humidity
                }
                return JsonResponse(data)
        except States.DoesNotExist:
            return JsonResponse({"error": "States object not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Invalid method"}, status=405)
    

from firebase_admin.messaging import Message as mm, Notification as bb, send

def send_push_notification(temperature,humidity):
    
    additional_data = {
        'temperature':temperature,
        'humidity': humidity,
        'type':'temperature'
        
        # Add more key-value pairs as needed
    }  
    message = mm(
           
            data=additional_data,
            token="dhOqShwLQGuo9US00HfFWr:APA91bGTMmoHnad4qeMc7viWY2_MejrUUFR8jb-VU02AUi53WOitQ7lxq1Pbvihrw3Nsq4WYoLtZAh-_X4nQdGC3uTF-fgXa4RlN5CaBkMEq76c4UOPu26MpyDsfK8NDkyk-XIGmcOhN",
        )
    

    response = send(message)

    print('Successfully sent message:', response)

def get_mode_state(request):
    CurrentMode = [] 
    mode = States.objects.get(pk=1)
    data = {
                    "name": mode.mode,
                }
    return JsonResponse(data) 
