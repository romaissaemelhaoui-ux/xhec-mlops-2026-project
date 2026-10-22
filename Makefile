install:
	uv sync
	uv run pre-commit install

lint:
	uv run pre-commit run --all-files

data:
	uv run kaggle datasets download rodolfomendes/abalone-dataset -p data --unzip

train:
	uv run python src/modelling/main.py data/abalone.csv

mlflow-ui:
	uv run mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5001

.PHONY: install lint data train mlflow-ui
