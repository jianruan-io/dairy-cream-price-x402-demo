import csv
import numpy as np
import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "usda_cream_classii_midwest_1996_2026.csv"

_df: pd.DataFrame | None = None


def load_cream_prices() -> pd.DataFrame:
    rows = []
    with open(DATA_PATH) as f:
        for r in csv.DictReader(f):
            if r["price_Unit"] != "Dollars per Pound":
                continue
            if not r["price_min"] or not r["price_max"]:
                continue
            rows.append({
                "date": pd.to_datetime(r["report_date"], format="%m/%d/%Y"),
                "price_min": float(r["price_min"]),
                "price_max": float(r["price_max"]),
            })

    df = pd.DataFrame(rows)
    df["price"] = (df["price_min"] + df["price_max"]) / 2
    df = (
        df.sort_values("date")
        .drop_duplicates(subset=["date"])
        .set_index("date")
    )
    return df


def get_df() -> pd.DataFrame:
    global _df
    if _df is None:
        _df = load_cream_prices()
    return _df


def get_prices() -> np.ndarray:
    return get_df()["price"].values
