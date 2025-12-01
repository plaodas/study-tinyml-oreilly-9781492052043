import numpy as np
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

def load_raw_csv(name: str) -> pd.DataFrame:
    """data/raw/{name}.csv を読み込むヘルパー。"""
    path = DATA_DIR / "raw" / f"{name}.csv"
    return pd.read_csv(path)

def save_processed_npz(name: str, x, y=None):
    """data/processed/{name}.npz に保存するヘルパー。"""
    path = DATA_DIR / "processed" / f"{name}.npz"
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(path, x=x, y=y)