from fastapi import FastAPI
from pydantic import BaseModel
from predict_utils import predict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Startup Funding Prediction API")

# -----------------------------
# ADD CORS MIDDLEWARE (FIX)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# REQUEST SCHEMA
# -----------------------------
class PredictionRequest(BaseModel):
    panel: str
    industry: str
    city: str
    founded_year: int
    no_of_founders: int
    funding_stage: str
    previous_funding_amount: float
    investment_type: str
    market_size_category: str

# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/")
def health_check():
    return {"status": "API is running"}

# -----------------------------
# PREDICTION ENDPOINT
# -----------------------------
@app.post("/predict")
def predict_funding(data: PredictionRequest):
    result = predict(data.dict())
    return result
