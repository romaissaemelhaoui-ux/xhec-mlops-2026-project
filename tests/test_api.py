"""Tests of the prediction API."""

from fastapi.testclient import TestClient

from src.web_service.main import app

client = TestClient(app)

# First row of the dataset (15 rings)
ABALONE = {
    "sex": "M",
    "length": 0.455,
    "diameter": 0.365,
    "height": 0.095,
    "whole_weight": 0.514,
    "shucked_weight": 0.2245,
    "viscera_weight": 0.101,
    "shell_weight": 0.15,
}


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200


def test_predict():
    response = client.post("/predict", json=ABALONE)
    assert response.status_code == 201
    prediction = response.json()
    assert prediction["rings"] > 0
    assert prediction["age"] == round(prediction["rings"] + 1.5, 2)


def test_predict_invalid_input():
    for wrong_field in [{"sex": "X"}, {"length": -1}]:
        response = client.post("/predict", json=ABALONE | wrong_field)
        assert response.status_code == 422
