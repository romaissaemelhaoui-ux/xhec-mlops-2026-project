"""Predict the number of rings with a trained model."""

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline


def predict(model: Pipeline, X: pd.DataFrame) -> np.ndarray:
    """Return the predicted number of rings for each abalone in `X`."""
    return model.predict(X)
