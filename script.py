# external_script.py




import os
import django
# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pfe.settings")
django.setup()

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from admin_soft.forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.models import User
import json
import joblib
from django.http import HttpResponse
import csv
import io
import time

import joblib
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

from smarthomeDataSets.models import *
MODEL_FILE_PATH_LIGHT = 'light_model.joblib' 
MODEL_FILE_PATH_WEATHER = 'weather_model.joblib' 
MODEL_FILE_PATH_WEATHER_SCALER = 'weather_model_scaler.joblib' 

MODEL_FILE_PATH_TV = 'tv_model.joblib' 
def create_model_light():
    start_time = time.time()
    queryset = lightDataSet.objects.all()
    # Create an in-memory file-like object (io.StringIO for Python 3)
    csv_buffer = io.StringIO()
    # Create a CSV writer object
    writer = csv.writer(csv_buffer)
    # Write headers
    field_names = [field.name for field in lightDataSet._meta.fields]
    writer.writerow(field_names)    
    # Write data rows
    for obj in queryset:
        row = [getattr(obj, field_name) for field_name in field_names]
        writer.writerow(row)
    # Seek to the beginning of the buffer
    csv_buffer.seek(0)
    # Read CSV data from buffer into pandas DataFrame
    dataset = pd.read_csv(csv_buffer)
    dataset['motionDetection'].replace(['No','Yes'],[0,1],inplace=True)
    dataset = dataset[['temperature','dayOfWeek','motionDetection','LightIntensity','active']]
    dataset['active'] = dataset['active'].replace({True: 1, False: 0})
    # Prepare data for training
    y = dataset['active']
    X = dataset.drop('active', axis=1)
    # Train the model
    best_hyperparameters = {'max_depth': 20, 'min_samples_leaf': 2, 'min_samples_split': 9}
# Train the model
    model = DecisionTreeClassifier(**best_hyperparameters)
    model.fit(X, y)
    
    # Predict using the trained model
    # probabilities, predicted_class = survive(model)

    end_time = time.time()
    execution_time = end_time - start_time
    print(execution_time)
    joblib.dump(model, MODEL_FILE_PATH_LIGHT)
    # Create instances of your model

def create_model_fan():
    start_time = time.time()
    
    # Fetch all data from the WeatherData model
    queryset = WeatherData.objects.all()
    
    # Create an in-memory file-like object
    csv_buffer = io.StringIO()
    
    # Create a CSV writer object
    writer = csv.writer(csv_buffer)
    
    # Write headers
    field_names = [field.name for field in WeatherData._meta.fields]
    writer.writerow(field_names)
    
    # Write data rows
    for obj in queryset:
        row = [getattr(obj, field_name) for field_name in field_names]
        writer.writerow(row)
    
    # Seek to the beginning of the buffer
    csv_buffer.seek(0)
    
    # Read CSV data from buffer into pandas DataFrame
    dataset = pd.read_csv(csv_buffer)
    
    # Convert time to seconds
    dataset['time'] = pd.to_datetime(dataset['time'], format='%H:%M:%S.%f').dt.hour * 3600 + pd.to_datetime(dataset['time'], format='%H:%M:%S.%f').dt.minute * 60 + pd.to_datetime(dataset['time'], format='%H:%M:%S.%f').dt.second 
    dataset = dataset.drop(columns=['month'])

    # Data Preprocessing
    dataset['motionDetection'].replace({False: 0, True: 1}, inplace=True)
    dataset = dataset.drop(columns=['id'])  # Assuming there is an 'id' column
    print(dataset)
    
    # Prepare data for training
    y = dataset['fanLevel']
    X = dataset.drop('fanLevel', axis=1)

    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Define the model with KNN
    knn = KNeighborsClassifier(n_neighbors=8, metric='manhattan')
    knn.fit(X_scaled, y)

        
    # Save the model and the scaler
    joblib.dump(knn, MODEL_FILE_PATH_WEATHER)
    joblib.dump(scaler, MODEL_FILE_PATH_WEATHER_SCALER)

    end_time = time.time()
    execution_time = end_time - start_time
    print(execution_time)
    # joblib.dump(knn, MODEL_FILE_PATH_WEATHER)


    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Model training completed in {execution_time} seconds")


def create_model_tv():
    start_time = time.time()
    queryset = TVDataSet.objects.all()
    
    # Create an in-memory file-like object (io.StringIO for Python 3)
    csv_buffer = io.StringIO()
    
    # Create a CSV writer object
    writer = csv.writer(csv_buffer)
    
    # Write headers
    field_names = [field.name for field in TVDataSet._meta.fields]
    writer.writerow(field_names)    
    
    # Write data rows
    for obj in queryset:
        row = [getattr(obj, field_name) for field_name in field_names]
        writer.writerow(row)
    
    # Seek to the beginning of the buffer
    csv_buffer.seek(0)
    
    # Read CSV data from buffer into pandas DataFrame
    dataset = pd.read_csv(csv_buffer)
    dataset['timeOfDay'] = pd.to_datetime(dataset['timeOfDay'], format='%H:%M:%S.%f').dt.hour * 3600 + pd.to_datetime(dataset['timeOfDay'], format='%H:%M:%S.%f').dt.minute * 60 + pd.to_datetime(dataset['timeOfDay'], format='%H:%M:%S.%f').dt.second 
    dataset = dataset.drop(columns=['id']) 
    # Convert boolean motionDetection field to binary
    dataset['motionDetection'] = dataset['motionDetection'].astype(int)
    print(dataset)
    # Prepare data for training
    y = dataset['channelOn']
    X = dataset.drop('channelOn', axis=1)
    
    # Train the model
    best_hyperparameters = {'max_depth': None, 'min_samples_leaf': 1, 'min_samples_split': 2, 'n_estimators': 100}
    model = RandomForestClassifier(**best_hyperparameters)
    model.fit(X, y)
    
    end_time = time.time()
    execution_time = end_time - start_time
    print(execution_time)
    
    joblib.dump(model, MODEL_FILE_PATH_TV)

if __name__ == "__main__":
  #  create_model_light()
#   create_model_fan()
    create_model_tv()
#    load_model()
