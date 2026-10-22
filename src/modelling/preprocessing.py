"""Read and prepare the abalone data."""

from pathlib import Path

import pandas as pd

TARGET = "Rings"


def load_data(path: Path) -> pd.DataFrame:
    """Read the abalone CSV and drop the rows with an impossible height of 0."""
    df = pd.read_csv(path)
    return df[df["Height"] > 0]


def split_features_target(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Separate the input features from the target (number of rings)."""
    return df.drop(columns=TARGET), df[TARGET]
