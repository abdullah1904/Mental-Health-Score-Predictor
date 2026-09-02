from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pathlib import Path
from models import PredictRequest, PredictResponse
from utils import load_model

model = load_model(Path(__file__).parent / "Mental_Health_Model.pkl")
top_countries = [ 
    'Other', 
    'India', 
    'USA', 
    'Canada', 
    'Australia', 
    'UK', 
    'Germany', 
    'Mexico',
    'Turkey',
    'France'
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the ML model API!"}

@app.post("/predict")
def predict(data: PredictRequest):
    country_group = data.country if data.country in top_countries else "Other"
    input_row = pd.DataFrame([{
        'Age' : data.age,
        'Gender' : data.gender,
        'Academic_Level' : data.academic_level,
        'Most_Used_Platform' : data.most_used_platform,
        'Purpose_Of_Use' : data.purpose_of_use,
        'Avg_Daily_Usage_Hours' : data.avg_daily_usage_hours,
        'Daily_Unlocks' : data.daily_unlocks,
        'Study_Hours' : data.study_hours,
        'Physical_Activity_Hours' : data.physical_activity_hours,
        'Sleep_Hours_Per_Night' : data.sleep_hours_per_night,
        'Stress_Level' : data.stress_level,
        'Grouped_Country' : country_group
    }])
    prediction = model.predict(input_row)[0]
    return PredictResponse(predicted_mental_health_score=round(float(prediction),2))