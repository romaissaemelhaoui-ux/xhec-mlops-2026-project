install:
	uv sync
	uv run pre-commit install

lint:
	uv run pre-commit run --all-files

data:
	uv run kaggle datasets download rodolfomendes/abalone-dataset -p data --unzip

mlflow-ui:
	uv run mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5001

.PHONY: install lint data mlflow-ui
