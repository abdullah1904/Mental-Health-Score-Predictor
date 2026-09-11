# Mental Health Score Predictor — Streamlit App

A simple Streamlit app that predicts a **Mental Health Score (0–10)** from
social media usage, sleep, study, and lifestyle habits, using a trained Random
Forest model.

Model: [abdullah1904/Mental-Health-Score-Predictor](https://huggingface.co/abdullah1904/Mental-Health-Score-Predictor) on Hugging Face.

## Features

- Streamlit form for easy predictions
- Request validation with Pydantic
- Loads a pre-trained scikit-learn pipeline (`Mental_Health_Model.pkl`)
- Auto-groups unseen countries into `"Other"` to match training data
- CORS enabled for frontend integration

## Project Structure

```bash
├── main.py       # Streamlit app and prediction logic
├── models.py     # Pydantic request/response schemas
├── utils.py      # model loading helper
├── Mental_Health_Model.pkl   # trained model
├── pyproject.toml
└── uv.lock
```

## Setup

```bash
git clone https://github.com/abdullah1904/Mental-Health-Score-Predictor.git
cd Mental-Health-Score-Predictor
uv sync
```

## Run

```bash
uv run streamlit run main.py
```

The app opens at `http://localhost:8501`.

Fill in the form and click **Predict score** to get a result.

### Field Constraints

| Field | Type | Constraints |
| --- | --- | --- |
| `age` | int | 10–100 |
| `gender` | enum | `Male`, `Female` |
| `country` | string | any (mapped to top-10 + "Other") |
| `academic_level` | enum | `Undergraduate`, `Graduate`, `High School` |
| `most_used_platform` | enum | Facebook, LinkedIn, Instagram, Snapchat, Twitter, YouTube, TikTok, LINE, KakaoTalk, VKontakte, WhatsApp, WeChat |
| `purpose_of_use` | enum | `Networking`, `Education`, `Entertainment`, `News` |
| `avg_daily_usage_hours` | float | 0–24 |
| `daily_unlocks` | int | ≥ 0 |
| `study_hours` | float | 0–24 |
| `physical_activity_hours` | float | 0–24 |
| `sleep_hours_per_night` | float | 0–24 |
| `stress_level` | enum | `Low`, `Medium`, `High`, `Very High` |

## Model Details

- **Algorithm:** Random Forest Regressor
- **Test R²:** 0.878 · **MAE:** 0.347 · **RMSE:** 0.464
- Full training notebook and dataset card on the [Hugging Face repo](https://huggingface.co/abdullah1904/Mental-Health-Score-Predictor)

## Disclaimer

Educational project only. Not a validated clinical or diagnostic tool.

## License

MIT
