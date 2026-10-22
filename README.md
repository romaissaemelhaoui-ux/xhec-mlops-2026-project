<div align="center">

# MLOps Project: Abalone Age Prediction

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)]()
[![Linting: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-informational?logo=pre-commit&logoColor=white)](.pre-commit-config.yaml)
</div>

## 🎯 Project Overview

The age of an abalone (a sea snail) is usually found by cutting its shell, staining it and counting the rings under a microscope, which is slow.
This project predicts the number of rings (age ≈ rings + 1.5 years) from easy-to-measure physical features (sex, size and weights), and turns the model into an MLOps system:

- **Training pipeline** with [Prefect](https://docs.prefect.io/), retraining the model every week
- **Prediction API** with [FastAPI](https://fastapi.tiangolo.com/), input validated with Pydantic, running in **Docker**
- **Experiment tracking** with [MLflow](https://mlflow.org/) in the modelling notebook
- **Code quality**: ruff (linter + formatter) with pre-commit hooks, run in the CI on every push and pull request

Dataset: [Abalone dataset on Kaggle](https://www.kaggle.com/datasets/rodolfomendes/abalone-dataset) (4,177 abalones).

## 👤 Team

| Name | GitHub |
|---|---|
| Romaissa Emelhaoui | [@romaissaemelhaoui-ux](https://github.com/romaissaemelhaoui-ux) |

## 📁 Project Structure

```
├── notebooks/
│   ├── eda.ipynb                # data exploration and conclusions
│   └── modelling.ipynb          # first models, tracked with MLflow
├── src/
│   ├── modelling/               # training pipeline (Prefect)
│   │   ├── preprocessing.py     # load the data, split features / target
│   │   ├── training.py          # one-hot encoding of Sex + linear regression (sklearn Pipeline)
│   │   ├── predicting.py        # predictions
│   │   ├── utils.py             # save objects with pickle
│   │   ├── main.py              # training flow
│   │   └── deployment.py        # weekly retraining deployment
│   └── web_service/             # prediction API (FastAPI)
│       ├── main.py              # API routes
│       ├── lib/models.py        # Pydantic input / output models
│       ├── lib/inference.py     # run the model on the API input
│       ├── utils.py             # load pickled objects
│       └── local_objects/       # trained model (model.pkl)
├── bin/run_services.sh          # starts the API and the Prefect server in the container
├── Dockerfile.app
└── Makefile                     # all the commands below
```

## 🚀 Setup

Prerequisites: Python 3.11, [uv](https://docs.astral.sh/uv/), [Docker Desktop](https://www.docker.com/products/docker-desktop/) (running) and, to download the data, a [Kaggle API token](https://www.kaggle.com/docs/api#authentication).

```bash
git clone https://github.com/romaissaemelhaoui-ux/xhec-mlops-2026-project.git
cd xhec-mlops-2026-project
make install   # creates .venv with all dependencies and installs the pre-commit hooks
make data      # downloads the dataset into data/
```

## 🌐 Prediction API (Docker)

A trained model is already included (`src/web_service/local_objects/model.pkl`), so the API can be started directly:

```bash
make docker-build   # builds the image "abalone-api"
make docker-run     # runs it: API on port 8000, Prefect UI on port 4200
```

- API documentation (try the endpoints in the browser): http://localhost:8000/docs
- Prefect UI: http://localhost:4200

Example of prediction:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sex": "M", "length": 0.455, "diameter": 0.365, "height": 0.095, "whole_weight": 0.514,
       "shucked_weight": 0.2245, "viscera_weight": 0.101, "shell_weight": 0.15}'
```

```json
{"rings": 9.22, "age": 10.72}
```

`sex` must be `M`, `F` or `I` (infant) and all measurements must be positive, otherwise the API answers with a `422` error explaining which field is wrong.

To run the API without Docker: `make api` (then http://localhost:8000/docs).

## 🤖 Training Pipeline (Prefect)

Train the model and save it to `src/web_service/local_objects/model.pkl`:

```bash
make train
```

The training is a Prefect flow (`src/modelling/main.py`): each step (load data, split, train, evaluate, save the model) is a Prefect task.

To retrain the model regularly:

1. Start the Prefect server, then open the UI at http://127.0.0.1:4200:

   ```bash
   make prefect-server
   ```

2. In a second terminal, start the deployment that retrains the model every Monday at midnight (UTC):

   ```bash
   make deploy
   ```

3. In the UI, go to **Deployments → train-model/weekly-retraining**: the upcoming runs are listed there. Click **Run → Quick run** to retrain now, and follow the flow and task runs in **Runs**.

Stop the Docker container first if it is running, as it also uses port 4200.

## 📊 Notebooks and Results

The notebooks in `notebooks/` use the project's `.venv` as kernel.

- **EDA**: the data is clean (no missing values). `Shell weight` is the measurement most correlated with the number of rings, and infants have fewer rings than adults. The 2 abalones with a height of 0 are removed.
- **Modelling**: a linear regression and a random forest were compared with MLflow. They perform the same (test RMSE ≈ 2.2 rings, R² ≈ 0.57), so the simpler linear regression is used.

To see the MLflow experiments:

```bash
make mlflow-ui   # then open http://127.0.0.1:5001
```

## ✅ Code Quality

```bash
make lint   # ruff linting/formatting and other pre-commit hooks
```

The same checks run in the GitHub Actions CI (`.github/workflows/ci.yaml`) on every push and pull request.

Dependencies are managed with uv in `pyproject.toml` and locked in `uv.lock`. To add one: `uv add <package>`.
