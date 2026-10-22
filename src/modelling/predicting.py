"""Predict the number of rings with a trained model."""

import numpy as np
import pandas as pd
from prefect import task
from sklearn.pipeline import Pipeline


@task
def predict(model: Pipeline, X: pd.DataFrame) -> np.ndarray:
    """Return the predicted number of rings for each abalone in `X`."""
    return model.predict(X)
