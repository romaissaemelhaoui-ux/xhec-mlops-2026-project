"""Build and train the model."""

import pandas as pd
from prefect import task
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def build_pipeline() -> Pipeline:
    """Chain the one-hot encoding of `Sex` with a linear regression."""
    preprocessor = ColumnTransformer(
        [("sex", OneHotEncoder(handle_unknown="ignore"), ["Sex"])],
        remainder="passthrough",
    )
    return Pipeline([("preprocessor", preprocessor), ("model", LinearRegression())])


@task
def train_model(X: pd.DataFrame, y: pd.Series) -> Pipeline:
    """Fit the pipeline (encoder + model) on the training data."""
    pipeline = build_pipeline()
    pipeline.fit(X, y)
    return pipeline
