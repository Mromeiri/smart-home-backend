# ⚡ Smart IoT Prediction Backend – Django & Machine Learning

This is the backend API powering the **Smart IoT Prediction System**, built with **Django, Django REST Framework (DRF), and Scikit-Learn**. It provides **real-time predictions** based on **sensor data** collected continuously, and it retrains the machine learning model **daily at midnight (00:00)** to adapt to new data dynamically.

## ✨ Features

* **Django REST API** – Provides endpoints for the mobile app to request predictions
* **Continuous Machine Learning Retraining** – A new model is generated **every day at 00:00** based on the latest sensor data
* **Real-Time Predictions** – Can **predict on-demand** when the mobile app requests or **automatically** at scheduled times
* **Optimized for IoT Sensors** – Designed to handle streaming sensor data efficiently
* **PostgreSQL for Data Storage** – Stores historical data and model versions
* **Celery & Redis for Background Tasks** – Ensures non-blocking training and prediction

## 🚀 Getting Started

### 📌 Prerequisites

Make sure you have the following installed:

* [Python 3.10+](https://www.python.org/)
* [Redis](https://redis.io/) (for Celery task queue)



## 🔬 Machine Learning Pipeline

### 📡 Data Flow

1. IoT Sensors continuously send data → Stored in PostgreSQL
2. At 00:00 every day, a new ML model is trained using the latest sensor data
3. The trained model is saved and used for the next 24 hours
4. Mobile App requests predictions → API processes request → Returns results

### 🛠 Model Training (ml/train_model.py)

* Uses Scikit-Learn for model training
* Runs automatically every day at 00:00 via Celery Beat
* Saves the trained model as a .pkl file for the next day's use
* Logs accuracy and training metrics


## 📡 API Endpoints


| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /switch_light/ | Toggle light state |
| GET | /switch_door/ | Toggle door state |
| GET | /get_light_state/ | Get light state |
| GET | /get_tv_state/ | Get TV state |
| GET | /get_fan_level/ | Get fan level |
| GET | /get_tv_state_name/ | Get TV state name |
| GET | /get_door_state/ | Get door state |
| POST | /set_temperature/<temperature>/<humidity>/ | Set temperature and humidity |
| GET | /get_temperature/ | Get current temperature and humidity |
| GET | /get_mode_state/ | Get current mode state |
| GET | /switch_mode/ | Switch mode |
| GET | /switch_tv_channel/ | Switch TV channel |
| GET | /switch_fan_level/ | Switch fan level |
| POST | /insert/<temperature>/<motion_detection>/<light_intensity>/<active>/ | Insert sensor data |
| POST | /insert_tv/<motionDetection>/<channelOn>/ | Insert TV data |
| POST | /insert_wether/<room_temperature>/<room_humidity>/<motionDetection>/<fanLevel>/ | Insert weather data |
| GET | /download_excel/ | Download data as Excel |
| GET | /download_csv/ | Download data as CSV |
| GET | /download_csv_tv/ | Download TV data as CSV |
| GET | /download_csv_wether/ | Download weather data as CSV |
| GET | /prediction_light/ | Predict light behavior |
| GET | /prediction_fan/ | Predict fan level |
| GET | /prediction_tv/ | Predict TV behavior |
| GET | /get_weather_json/ | Get weather data in JSON format |



### Example Prediction Request
```sh
curl -X GET "http://127.0.0.1:8000/prediction_light"
```

### Example Response
```json
{
  "prediction": 18.7,
  "model_used": "model_2025-02-14.pkl",
  "timestamp": "2025-02-14T10:00:00Z"
}
```

## 🚀 Background Tasks with Celery

| Task | Description | Schedule |
|------|-------------|----------|
| train_and_save_model() | Retrains model every day at 00:00 | Daily |
| predict_on_new_data() | Auto-predicts when new sensor data arrives | On event |

## 🛠 Technologies Used

* Backend: Django, Django REST Framework (DRF)
* Machine Learning: Scikit-Learn
* Database: SQLite
* Task Queue: Celery + Redis

## 🎯 Future Improvements

* WebSockets for real-time predictions
* Deploy to AWS Lambda or FastAPI for speed
* Improve model selection dynamically
* Secure urls with JWT token

## 💡 Contributing

Feel free to fork this repo and submit a PR. Contributions are always welcome!

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

### 📌 Summary of What's Covered:
* **Django REST API** with machine learning predictions
* **Scikit-Learn** training every day at **00:00**
* **API Endpoints for mobile app** to request predictions
* **Celery & Redis** for background ML retraining

🚀 Smart IoT Predictions – Adaptive ML for Real-Time IoT Insights!
