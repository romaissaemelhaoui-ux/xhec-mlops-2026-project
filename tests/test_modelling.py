"""Tests of the training code, on a small fake dataset (the real one is not in the repo)."""

import pandas as pd

from src.modelling.preprocessing import load_data, split_features_target
from src.modelling.training import build_pipeline

DATA = pd.DataFrame(
    {
        "Sex": ["M", "F", "I", "M", "I"],
        "Length": [0.45, 0.53, 0.33, 0.44, 0.3],
        "Diameter": [0.36, 0.42, 0.25, 0.36, 0.22],
        "Height": [0.09, 0.13, 0.08, 0.0, 0.07],
        "Whole weight": [0.51, 0.68, 0.2, 0.51, 0.15],
        "Shucked weight": [0.22, 0.26, 0.09, 0.22, 0.06],
        "Viscera weight": [0.1, 0.14, 0.04, 0.11, 0.03],
        "Shell weight": [0.15, 0.21, 0.07, 0.15, 0.05],
        "Rings": [15, 9, 7, 10, 6],
    }
)


def test_load_data_removes_zero_height(tmp_path):
    path = tmp_path / "abalone.csv"
    DATA.to_csv(path, index=False)
    df = load_data.fn(path)  # .fn calls the function without Prefect
    assert len(df) == 4
    assert (df["Height"] > 0).all()


def test_pipeline_trains_and_predicts():
    X, y = split_features_target.fn(DATA)
    assert "Rings" not in X.columns
    model = build_pipeline().fit(X, y)
    assert len(model.predict(X)) == len(X)
