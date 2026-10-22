"""Training flow: read the data, preprocess it, train a model and save it."""

import argparse
from pathlib import Path

from predicting import predict
from preprocessing import load_data, split_features_target
from sklearn.metrics import root_mean_squared_error
from sklearn.model_selection import train_test_split
from training import train_model
from utils import pickle_object

MODEL_PATH = Path(__file__).parents[1] / "web_service" / "local_objects" / "model.pkl"


def main(trainset_path: Path) -> None:
    """Train a model using the data at the given path and save it (pickle)."""
    df = load_data(trainset_path)
    X, y = split_features_target(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = train_model(X_train, y_train)
    rmse = root_mean_squared_error(y_test, predict(model, X_test))
    print(f"Test RMSE: {rmse:.2f} rings")

    pickle_object(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train a model using the data at the given path."
    )
    parser.add_argument("trainset_path", type=Path, help="Path to the training set")
    args = parser.parse_args()
    main(args.trainset_path)
