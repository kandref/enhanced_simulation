from __future__ import annotations

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {"periode_data", "bulan", "nama_jalan", "kecepatan"}


def load_corridor_speed(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    cleaned = df.copy()
    cleaned["year"] = cleaned["periode_data"].astype(int)
    cleaned["month"] = cleaned["bulan"].astype(int)
    cleaned["corridor"] = cleaned["nama_jalan"].astype(str).str.strip()
    cleaned["speed_kmh"] = (
        cleaned["kecepatan"].astype(str).str.replace(",", ".", regex=False).astype(float)
    )
    cleaned["date"] = pd.to_datetime(
        {
            "year": cleaned["year"],
            "month": cleaned["month"],
            "day": 1,
        }
    )
    return cleaned[["date", "year", "month", "corridor", "speed_kmh"]].sort_values(
        ["corridor", "date"]
    )


def summarize_corridors(speed_df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        speed_df.groupby("corridor", as_index=False)
        .agg(
            mean_speed_kmh=("speed_kmh", "mean"),
            min_speed_kmh=("speed_kmh", "min"),
            max_speed_kmh=("speed_kmh", "max"),
            observations=("speed_kmh", "size"),
        )
        .sort_values("mean_speed_kmh")
        .reset_index(drop=True)
    )
    summary["bottleneck_rank"] = summary.index + 1
    return summary[
        [
            "bottleneck_rank",
            "corridor",
            "mean_speed_kmh",
            "min_speed_kmh",
            "max_speed_kmh",
            "observations",
        ]
    ]


def monthly_summary(speed_df: pd.DataFrame) -> pd.DataFrame:
    return (
        speed_df.groupby(["year", "month"], as_index=False)
        .agg(
            mean_speed_kmh=("speed_kmh", "mean"),
            min_speed_kmh=("speed_kmh", "min"),
            max_speed_kmh=("speed_kmh", "max"),
            corridors=("corridor", "nunique"),
        )
        .sort_values(["year", "month"])
    )
