"""Save and load Python objects with pickle."""

import pickle
from pathlib import Path
from typing import Any


def pickle_object(obj: Any, path: Path) -> None:
    """Save `obj` to `path` in pickle format."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(obj, f)


def load_pickle(path: Path) -> Any:
    """Load a pickled object from `path`."""
    with open(path, "rb") as f:
        return pickle.load(f)
