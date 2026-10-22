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

api:
	uv run uvicorn src.web_service.main:app --port 8000

docker-build:
	docker build -f Dockerfile.app -t abalone-api .

docker-run:
	docker run --rm -p 0.0.0.0:8000:8001 -p 0.0.0.0:4200:4201 abalone-api

mlflow-ui:
	uv run mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5001

.PHONY: install lint data train prefect-server deploy api docker-build docker-run mlflow-ui
