"""Pydantic models for the web service."""

from typing import Literal

from pydantic import BaseModel, Field


class AbaloneInput(BaseModel):
    """Physical measurements of an abalone (lengths in mm / 200, weights in g / 200)."""

    # Example shown in the API docs (/docs), taken from the first row of the dataset
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sex": "M",
                    "length": 0.455,
                    "diameter": 0.365,
                    "height": 0.095,
                    "whole_weight": 0.514,
                    "shucked_weight": 0.2245,
                    "viscera_weight": 0.101,
                    "shell_weight": 0.15,
                }
            ]
        }
    }

    sex: Literal["M", "F", "I"] = Field(
        description="M (male), F (female) or I (infant)"
    )
    length: float = Field(gt=0)
    diameter: float = Field(gt=0)
    height: float = Field(gt=0)
    whole_weight: float = Field(gt=0)
    shucked_weight: float = Field(gt=0)
    viscera_weight: float = Field(gt=0)
    shell_weight: float = Field(gt=0)


class PredictionOutput(BaseModel):
    """Predicted number of rings and the corresponding age in years."""

    rings: float
    age: float
