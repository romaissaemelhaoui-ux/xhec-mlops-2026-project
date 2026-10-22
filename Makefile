install:
	uv sync
	uv run pre-commit install

lint:
	uv run pre-commit run --all-files

data:
	uv run kaggle datasets download rodolfomendes/abalone-dataset -p data --unzip

train:
	uv run python src/modelling/main.py data/abalone.csv

prefect-server:
	uv run prefect server start

deploy:
	PREFECT_API_URL=http://127.0.0.1:4200/api uv run python src/modelling/deployment.py

mlflow-ui:
	uv run mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5001

.PHONY: install lint data train prefect-server deploy mlflow-ui
