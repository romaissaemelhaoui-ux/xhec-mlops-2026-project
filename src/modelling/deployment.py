"""Deployment that retrains the model every week with Prefect."""

from pathlib import Path

from main import main

TRAINSET_PATH = Path(__file__).parents[2] / "data" / "abalone.csv"


if __name__ == "__main__":
    main.serve(
        name="weekly-retraining",
        cron="0 0 * * 1",  # every Monday at midnight
        parameters={"trainset_path": str(TRAINSET_PATH)},
    )
