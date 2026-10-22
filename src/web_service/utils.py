"""Utils for the web service."""

import pickle
from pathlib import Path
from typing import Any


def load_object(path: Path) -> Any:
    """Load a pickled object from `path`."""
    with open(path, "rb") as f:
        return pickle.load(f)
