from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"

def load_dataset(name: str) -> pd.DataFrame:
    """data/raw/{name}.csv を DataFrame として読み込む。"""
    return pd.read_csv(DATA_RAW / f"{name}.csv")

def train_test_scale(
    df: pd.DataFrame,
    label_col: str,
    test_size: float = 0.2,
    random_state: int = 42,
):
    """
    ラベル列を指定して train/test 分割 + 標準化を行う。
    """
    X = df.drop(columns=[label_col]).values
    y = df[label_col].values
    x_train, x_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)
    return (x_train, y_train), (x_test, y_test), scaler

def save_npz(name: str, x_train, y_train, x_test, y_test):
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        DATA_PROCESSED / f"{name}.npz",
        x_train=x_train,
        y_train=y_train,
        x_test=x_test,
        y_test=y_test,
    )