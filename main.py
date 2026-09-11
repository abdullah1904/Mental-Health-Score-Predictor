import pandas as pd
import streamlit as st
from pathlib import Path
from models import PredictRequest, PredictResponse
from utils import load_model

model = load_model(Path(__file__).parent / "Mental_Health_Model.pkl")
top_countries = [
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
country_options = top_countries + ['Other']

def predict(data: PredictRequest) -> PredictResponse:
    country_group = data.country if data.country in top_countries else "Other"
    input_row = pd.DataFrame([{
        'Age': data.age,
        'Gender': data.gender,
        'Academic_Level': data.academic_level,
        'Most_Used_Platform': data.most_used_platform,
        'Purpose_Of_Use': data.purpose_of_use,
        'Avg_Daily_Usage_Hours': data.avg_daily_usage_hours,
        'Daily_Unlocks': data.daily_unlocks,
        'Study_Hours': data.study_hours,
        'Physical_Activity_Hours': data.physical_activity_hours,
        'Sleep_Hours_Per_Night': data.sleep_hours_per_night,
        'Stress_Level': data.stress_level,
        'Grouped_Country': country_group
    }])
    prediction = model.predict(input_row)[0]
    return PredictResponse(predicted_mental_health_score=round(float(prediction), 2))


def display_prediction_card(score: float) -> None:
    if score <= 5:
        color = "#dc2626"
        background = "#fef2f2"
        status = "Needs attention"
    elif score <= 8:
        color = "#ca8a04"
        background = "#fefce8"
        status = "Moderate range"
    else:
        color = "#16a34a"
        background = "#f0fdf4"
        status = "Healthy range"

    st.markdown(
        f"""
        <div style="
            border: 2px solid {color};
            border-radius: 14px;
            background: {background};
            padding: 1.25rem;
            margin: 1.5rem 0 0.5rem;
            text-align: center;
        ">
            <div style="color: {color}; font-size: 1rem; font-weight: 600;">{status}</div>
            <div style="color: {color}; font-size: 3rem; font-weight: 700; line-height: 1.2;">{score:.2f}</div>
            <div style="color: #475569; font-size: 0.95rem;">Mental health score out of 10</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.set_page_config(
    page_title="Mental Health Score Predictor",
    page_icon="🧠",
    layout="wide",
)
st.markdown(
    """
    <style>
        [data-testid="stForm"] {
            width: 100%;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
st.title("Mental Health Score Predictor")
st.caption("Estimate a score from 0 to 10 using lifestyle and social media habits.")

with st.form("prediction_form"):
    first_row = st.columns(3)
    with first_row[0]:
        age = st.number_input("Age", min_value=10, max_value=100, value=None, step=1, placeholder="Enter age")
    with first_row[1]:
        gender = st.selectbox("Gender", ["Male", "Female"], index=None, placeholder="Select gender")
    with first_row[2]:
        country = st.selectbox("Country", country_options, index=None, placeholder="Select country")

    second_row = st.columns(3)
    with second_row[0]:
        academic_level = st.selectbox("Academic level", ["Undergraduate", "Graduate", "High School"], index=None, placeholder="Select academic level")
    with second_row[1]:
        most_used_platform = st.selectbox("Most used platform", [
            "Facebook", "LinkedIn", "Instagram", "Snapchat", "Twitter", "YouTube",
            "TikTok", "LINE", "KakaoTalk", "VKontakte", "WhatsApp", "WeChat"
        ], index=None, placeholder="Select platform")
    with second_row[2]:
        purpose_of_use = st.selectbox("Purpose of use", ["Networking", "Education", "Entertainment", "News"], index=None, placeholder="Select purpose")

    third_row = st.columns(3)
    with third_row[0]:
        avg_daily_usage_hours = st.number_input("Average daily usage (hours)", min_value=0.0, max_value=24.0, value=None, step=0.5, placeholder="Enter hours")
    with third_row[1]:
        daily_unlocks = st.number_input("Daily unlocks", min_value=0, value=None, step=1, placeholder="Enter unlocks")
    with third_row[2]:
        study_hours = st.number_input("Study hours per day", min_value=0.0, max_value=24.0, value=None, step=0.5, placeholder="Enter hours")

    fourth_row = st.columns(3)
    with fourth_row[0]:
        physical_activity_hours = st.number_input("Physical activity hours per day", min_value=0.0, max_value=24.0, value=None, step=0.5, placeholder="Enter hours")
    with fourth_row[1]:
        sleep_hours_per_night = st.number_input("Sleep hours per night", min_value=0.0, max_value=24.0, value=None, step=0.5, placeholder="Enter hours")
    with fourth_row[2]:
        stress_level = st.selectbox("Stress level", ["Low", "Medium", "High", "Very High"], index=None, placeholder="Select stress level")

    submitted = st.form_submit_button("Predict score", type="primary")

if submitted:
    form_values = {
        "Age": age,
        "Gender": gender,
        "Country": country,
        "Academic level": academic_level,
        "Most used platform": most_used_platform,
        "Purpose of use": purpose_of_use,
        "Average daily usage (hours)": avg_daily_usage_hours,
        "Daily unlocks": daily_unlocks,
        "Study hours per day": study_hours,
        "Physical activity hours per day": physical_activity_hours,
        "Sleep hours per night": sleep_hours_per_night,
        "Stress level": stress_level,
    }
    missing_fields = [field for field, value in form_values.items() if value is None]

    if missing_fields:
        st.error("Please complete the following fields: " + ", ".join(missing_fields))
    else:
        try:
            request = PredictRequest(
                age=age,
                gender=gender,
                country=country,
                academic_level=academic_level,
                most_used_platform=most_used_platform,
                purpose_of_use=purpose_of_use,
                avg_daily_usage_hours=avg_daily_usage_hours,
                daily_unlocks=daily_unlocks,
                study_hours=study_hours,
                physical_activity_hours=physical_activity_hours,
                sleep_hours_per_night=sleep_hours_per_night,
                stress_level=stress_level,
            )
            result = predict(request)
            display_prediction_card(result.predicted_mental_health_score)
        except Exception as error:
            st.error(f"Unable to make a prediction: {error}")