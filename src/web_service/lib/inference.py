"""Run the model on the data received by the API."""

import pandas as pd
from sklearn.pipeline import Pipeline

from src.web_service.lib.models import AbaloneInput

# API field name -> column name used when the model was trained
COLUMNS = {
    "sex": "Sex",
    "length": "Length",
    "diameter": "Diameter",
    "height": "Height",
    "whole_weight": "Whole weight",
    "shucked_weight": "Shucked weight",
    "viscera_weight": "Viscera weight",
    "shell_weight": "Shell weight",
}


def predict_rings(model: Pipeline, abalone: AbaloneInput) -> float:
    """Predict the number of rings of one abalone."""
    X = pd.DataFrame([abalone.model_dump()]).rename(columns=COLUMNS)
    return float(model.predict(X)[0])
