from app.core.database import get_db
from fastapi import APIRouter, Depends, HTTPException,Request
from sqlalchemy.orm import Session
from app.schemas.Order import AddOrder
from app.models.Order import Order
from datetime import datetime
from app.api.auth import get_current_user
from app.schemas.Prediction import DeliveryPredictionRequest
import joblib
import pandas as pd 
from dotenv import load_dotenv
import os
import requests


OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
lon=-9.503141
lat=30.348553

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "uploads", "delivery_model2.pkl")
model = joblib.load(model_path)

prediction_router = APIRouter()

@prediction_router.post('/predict')
def predict(prediction:DeliveryPredictionRequest,db: Session = Depends(get_db)
            # ,user=Depends(get_current_user)
            ):
    data=pd.DataFrame([prediction.model_dump()])
    data=pd.get_dummies(data)
    model_columns=model.feature_names_in_
    for col in model_columns:
        if col not in data.columns:
            data[col]=0
    data=data[model_columns]
    new_prediction=model.predict(data)
    # return new_prediction
    return {"new_prediction":new_prediction.tolist()}


@prediction_router.post('/get_weather')
def get_weather():
    url=f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    response=requests.get(url)
    data=response.json()
    return data