"""FastAPI app that predicts the age of an abalone."""

from pathlib import Path

from fastapi import FastAPI

from src.web_service.lib.inference import predict_rings
from src.web_service.lib.models import AbaloneInput, PredictionOutput
from src.web_service.utils import load_object

MODEL_PATH = Path(__file__).parent / "local_objects" / "model.pkl"

app = FastAPI(
    title="Abalone age prediction",
    description="Predict the number of rings (and the age) of an abalone from its measurements.",
)
model = load_object(MODEL_PATH)


@app.get("/")
def home() -> dict:
    return {"health_check": "App up and running!"}


@app.post("/predict", response_model=PredictionOutput, status_code=201)
def predict(payload: AbaloneInput) -> PredictionOutput:
    rings = predict_rings(model, payload)
    return PredictionOutput(rings=round(rings, 2), age=round(rings + 1.5, 2))
