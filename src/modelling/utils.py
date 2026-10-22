"""Save Python objects with pickle."""

import pickle
from pathlib import Path
from typing import Any

from prefect import task


@task
def pickle_object(obj: Any, path: Path) -> None:
    """Save `obj` to `path` in pickle format."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(obj, f)
