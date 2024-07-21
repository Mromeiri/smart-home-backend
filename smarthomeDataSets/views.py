# In views.py

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from states.models import States
from users.models import AppUser, NotificationML
from .models import *
from admin_soft.forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.models import User
import json
import joblib
MODEL_FILE_PATH_LIGHT = 'light_model.joblib' 
MODEL_FILE_PATH_WEATHER = 'weather_model.joblib' 
MODEL_FILE_PATH_WEATHER_SCALER = 'weather_model_scaler.joblib' 

MODEL_FILE_PATH_TV = 'tv_model.joblib' 
def admin_logout(request):
    logout(request)
    # Redirect to the admin login page or another suitable location
    return redirect('/admin/login/?next=/admin/')
def index(request):
    # Your view logic here
    return render(request, 'index.html')

# class TopFournisseur(View):
#     def get(self, request , *args **)
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # Check if a user with the provided email already exists
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'This email is already in use. Please choose another one.')
            else:
                # Create a new user only if the email is not already registered
                form.save()
                print('Account created successfully!')
                return redirect('/admin/login/?next=/admin/')
        else:
            print("Registration failed!")
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'accounts/register.html', context)
import requests


def get_weather(latitude, longitude, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data
def get_weather_json(request):
    latitude = 36.740509
    longitude = 3.115857
    api_key = '30d4741c779ba94c470ca1f63045390a'
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    print(data['visibility'])
    return JsonResponse(data)

@csrf_exempt
def insert_data(request, temperature, motion_detection, light_intensity,active):
    latitude = 36.740509
    longitude = 3.115857
    api_key = '30d4741c779ba94c470ca1f63045390a'
    weather_desc ='' 
    if latitude and longitude:
        weather_data = get_weather(latitude, longitude, api_key)
        weather_desc = weather_data['weather'][0]['description']
    if request.method == 'GET':
        try:
            # Convert data types if necessary
            temperature = float(temperature)
            light_intensity = float(light_intensity)

            # Create a new record in the lightDataSet model
            light_data = lightDataSet.objects.create(
                temperature=temperature,
                weatherConditions=weather_desc,
                motionDetection=motion_detection,
                LightIntensity=light_intensity,
                active =active
            )
            return HttpResponse("Data inserted successfully!")
        except Exception as e:
            return HttpResponse(f"Error: {e}", status=400)
    else:
        return HttpResponse("Invalid method", status=405)

@csrf_exempt
def insert_tv(request, motionDetection, channelOn):

    if request.method == 'GET':
        try:

            tv_data = TVDataSet.objects.create(
                motionDetection=motionDetection,
                channelOn=channelOn,
             
            )
            return HttpResponse("Data TV inserted successfully!")
        except Exception as e:
            return HttpResponse(f"Error: {e}", status=400)
    else:
        return HttpResponse("Invalid method", status=405)

@csrf_exempt
def insert_wether(request, room_temperature, room_humidity,motionDetection,fanLevel):

    if request.method == 'GET':
        try:

            wether_data = WeatherData.objects.create(
                room_temperature=room_temperature,
                room_humidity=room_humidity,
                motionDetection=motionDetection,
                fanLevel=fanLevel,
             
            )
            return HttpResponse("Data wether inserted successfully!")
        except Exception as e:
            return HttpResponse(f"Error: {e}", status=400)
    else:
        return HttpResponse("Invalid method", status=405)


from django.http import HttpResponse
import csv
from .models import lightDataSet

def download_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="light_dataset.csv"'

    writer = csv.writer(response)

    # Get field names including 'id'
    field_names = [field.name for field in lightDataSet._meta.fields]

    # Write header row with all attribute names
    writer.writerow(field_names)

    # Write data rows
    queryset = lightDataSet.objects.all()
    for obj in queryset:
        # Collect values for each field in a list
        row = [getattr(obj, field_name) for field_name in field_names]
        # Write the row to the CSV file
        writer.writerow(row)
    

    return response
def download_csv_tv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tv_dataSert.csv"'

    writer = csv.writer(response)

    # Get field names including 'id'
    field_names = [field.name for field in TVDataSet._meta.fields]

    # Write header row with all attribute names
    writer.writerow(field_names)

    # Write data rows
    queryset = TVDataSet.objects.all()
    for obj in queryset:
        # Collect values for each field in a list
        row = [getattr(obj, field_name) for field_name in field_names]
        # Write the row to the CSV file
        writer.writerow(row)
    

    return response
def download_csv_wether(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="wether_dataset.csv"'

    writer = csv.writer(response)

    # Get field names including 'id'
    field_names = [field.name for field in WeatherData._meta.fields]

    # Write header row with all attribute names
    writer.writerow(field_names)

    # Write data rows
    queryset = WeatherData.objects.all()
    for obj in queryset:
        # Collect values for each field in a list
        row = [getattr(obj, field_name) for field_name in field_names]
        # Write the row to the CSV file
        writer.writerow(row)
    

    return response
from django.http import HttpResponse
import pandas as pd
def download_excel(request):
    # Retrieve data from the model
    data = lightDataSet.objects.all()

    # Convert data to a DataFrame
    df = pd.DataFrame(list(data.values()))

    # Create an Excel writer object
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="light_data.xlsx"'

    # Write DataFrame to the response as Excel
    df.to_excel(response, index=False)

    return response


import io
import pandas as pd
from sys import displayhook
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
import time

# Start time measurement

from django.http import JsonResponse
import time

def doPredLight(request,):
    start_time = time.time()
    model = joblib.load(MODEL_FILE_PATH_LIGHT)

    # Example input data
    # Replace this with your actual input data for prediction
    state = States.objects.get(pk=1)
    input_data = {
        'temperature': state.temperature,
        'dayOfWeek': datetime.now().isoweekday(),  # Assuming 2 represents Tuesday
        'motionDetection': [1],  # 1 for Yes
        'LightIntensity': [300]
    }

    # Convert the input data to a pandas DataFrame
    input_df = pd.DataFrame(input_data)

    # Predict using the loaded model
    predicted_probabilities = model.predict_proba(input_df)
    predicted_class = model.predict(input_df)
    probabilities = model.predict_proba(input_df)[0]
    # Display the predictions
    print(f"Predicted probabilities: {predicted_probabilities}")
    print(f"Predicted class: {predicted_class}")

    # Prepare response
    end_time = time.time()
    execution_time = end_time - start_time
    # Prepare response
    if (int(predicted_class)==0 and state.light==True)or(int(predicted_class)==1 and state.light==False):
        if state.mode=="Smart Mode":
            state.light = not state.light
            state.save()
            print("we change it directly")
        elif state.mode=="Assisted Mode":
            user = AppUser.objects.get(username="omeiri.abdellah")
            notificaion = NotificationML.objects.create(
                date=datetime.now(),
                title="ML",
                detail="",
                user=user,
                itemControlled="light",
                classWantedToApply=str(int(predicted_class))



            
            )
            print("we send a notificaion")
        else:
            print("we do nothing")
        
    result = {
        "Predicted class": int(predicted_class),
        "probability_class0": float(probabilities[0]),
        "probability_class1": float(probabilities[1]),
        "execution Time":execution_time ,
    }


    return JsonResponse(result)

import joblib
import pandas as pd
import json
from django.http import JsonResponse
import time
from django.utils import timezone

def predict_fan_level(request):
    # Load the saved model and scaler
    knn = joblib.load(MODEL_FILE_PATH_WEATHER)
    scaler = joblib.load(MODEL_FILE_PATH_WEATHER_SCALER)

    # Create a dictionary with the input data
    latitude = 36.740509
    longitude = 3.115857
    api_key = '30d4741c779ba94c470ca1f63045390a'
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    print(data['main']['temp'])

    state = States.objects.get(pk=1)
    current_timee = timezone.now().time()
    current_time_in_seconds = (current_timee.hour * 3600 
                                + current_timee.minute * 60 
                                + current_timee.second 
                                )    
    print(current_time_in_seconds)
    input_data = {
        "time": current_timee,
        "day": datetime.now().isoweekday(),
        "outside_temperature": data['main']['temp'],
        "room_temperature": state.temperature,
        "outside_humidity": data['main']['humidity'],
        "room_humidity": state.humidity,
        "outside_luminosity": data['visibility'],
        "motionDetection": 0
    }

    # Convert input data to DataFrame
    input_df = pd.DataFrame([input_data])

    # Convert time to seconds
    input_df['time'] = pd.to_datetime(input_df['time'], format='%H:%M:%S.%f').dt.hour * 3600 + \
                        pd.to_datetime(input_df['time'], format='%H:%M:%S.%f').dt.minute * 60 + \
                        pd.to_datetime(input_df['time'], format='%H:%M:%S.%f').dt.second 
    # Replace motionDetection boolean with integers
    input_df['motionDetection'].replace({False: 0, True: 1}, inplace=True)

    

    # Standardize the features
    # X_scaled = scaler.transform(input_df)

    # Start timing the prediction process
    start_time = time.time()

    # Predict the class probabilities
    

    probabilities = knn.predict_proba(input_df)
    predicted_class = knn.predict(input_df)
    # Calculate execution time
    end_time = time.time()
    execution_time = end_time - start_time
    # Prepare the response
    if int(predicted_class)!=state.fanLevel:
        if state.mode=="Smart Mode":
            state.fanLevel=int(predicted_class)
            state.save()
            # state.light = not state.light
            # state.save()
            print("we change it directly")
        elif state.mode=="Assisted Mode":
            user = AppUser.objects.get(username="omeiri.abdellah")
            notificaion = NotificationML.objects.create(
                date=datetime.now(),
                title="ML",
                detail="",
                user=user,
                itemControlled="weather",
                classWantedToApply=str(int(predicted_class))



            
            )
            print("we send a notificaion")
        else:
            print("we do nothing")
    else:
        print("we do nothing cause same state")
    response = {
        "predicted_class": int(predicted_class[0]),
        # "probability_truee": float(predicted_probabilities[0]),
        "probability_class0": float(probabilities[0][0]),
        "probability_class1": float(probabilities[0][1]),
        "probability_class2": float(probabilities[0][2]),
        "probability_class3": float(probabilities[0][3]),
        "execution_time": execution_time
    }

    return JsonResponse(response)



def doPredTV(request):
    start_time = time.time()

    # Load the trained model
    model = joblib.load(MODEL_FILE_PATH_TV)

    # Example input data
    # Replace this with your actual input data for prediction
    state = TVDataSet.objects.get(pk=1)  # Assuming you want to predict for a specific instance
    current_timee = timezone.now().time()

    input_data = {
        'timeOfDay': [current_timee],
        'dayOfWeek': datetime.now().isoweekday(),  # Assuming 2 represents Tuesday
        'motionDetection': [1],  # 1 for Yes
    }

    # Convert the input data to a pandas DataFrame
    input_df = pd.DataFrame(input_data)
    input_df['timeOfDay'] = pd.to_datetime(input_df['timeOfDay'], format='%H:%M:%S.%f').dt.hour * 3600 + \
                        pd.to_datetime(input_df['timeOfDay'], format='%H:%M:%S.%f').dt.minute * 60 + \
                        pd.to_datetime(input_df['timeOfDay'], format='%H:%M:%S.%f').dt.second 
    # Predict using the loaded model
    predicted_probabilities = model.predict_proba(input_df)
    predicted_class = model.predict(input_df)
    probabilities = predicted_probabilities[0]

    # Display the predictions
    print(f"Predicted probabilities: {predicted_probabilities}")
    print(f"Predicted class: {predicted_class}")

    # Prepare response
    end_time = time.time()
    execution_time = end_time - start_time
    state = States.objects.get(pk=1)
    if int(predicted_class)!=state.channelOn:
        if state.mode=="Smart Mode":
            state.channelOn=int(predicted_class)
            state.channelName=""
            state.save()
            # state.light = not state.light
            # state.save()
            print("we change it directly")
        elif state.mode=="Assisted Mode":
            user = AppUser.objects.get(username="omeiri.abdellah")
            notificaion = NotificationML.objects.create(
                date=datetime.now(),
                title="ML",
                detail="",
                user=user,
                itemControlled="tv",
                classWantedToApply=str(int(predicted_class))



            
            )
            print("we send a notificaion")
        else:
            print("we do nothing")
    else:
        print("we do nothing cause same state")
    # Prepare response
    result = {
        "Predicted class": int(predicted_class),
        "probability_class0": float(probabilities[0]),
        "probability_class1": float(probabilities[1]),
        "probability_class2": float(probabilities[2]),
        "probability_class3": float(probabilities[3]),
        "probability_class4": float(probabilities[4]),
        "probability_class5": float(probabilities[5]),
        "probability_class6": float(probabilities[6]),


        "execution Time": execution_time,
    }

    return JsonResponse(result)