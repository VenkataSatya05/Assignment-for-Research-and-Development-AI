import pandas as pd
from pathlib import Path
from typing import Tuple
import json # Added import for 'json' in the global scope if it's used elsewhere, otherwise it's fine inside save_results




def load_xy(path: str) -> pd.DataFrame:
    """Load xy CSV and validate columns.

    Expected columns: x, y (optionally t)
    """
    p = Path(path)
    df = pd.read_csv(p)
    expected = {"x", "y"}
    if not expected.issubset(df.columns):
        raise ValueError(f"CSV must contain columns: {expected}. Found: {list(df.columns)}")
    return df


def save_results(params: dict, out_path: str):
    import json # Although imported above, keeping it here as it was in your original structure
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w") as f:
        json.dump(params, f, indent=2)