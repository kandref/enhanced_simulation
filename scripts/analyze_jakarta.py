from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from traffic_fluid_model.jakarta_data import (
    load_corridor_speed,
    monthly_summary,
    summarize_corridors,
)


RAW_SPEED_PATH = ROOT / "data" / "raw" / "jakarta_41_corridor_peak_speed.csv"
PROCESSED_DIR = ROOT / "data" / "processed"
FIGURE_DIR = ROOT / "results" / "figures"


def plot_slowest_corridors(summary, path: Path, n: int = 12) -> None:
    slowest = summary.head(n).sort_values("mean_speed_kmh")
    fig, ax = plt.subplots(figsize=(9, 5.8))
    ax.barh(slowest["corridor"], slowest["mean_speed_kmh"], color="tab:red")
    ax.set_title("Jakarta Slowest Peak-Hour Corridors")
    ax.set_xlabel("Mean speed (km/h)")
    ax.set_ylabel("Corridor")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, dpi=170)
    plt.close(fig)


def plot_monthly_speed(monthly, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.plot(monthly["month"], monthly["mean_speed_kmh"], marker="o", label="Mean")
    ax.fill_between(
        monthly["month"],
        monthly["min_speed_kmh"],
        monthly["max_speed_kmh"],
        alpha=0.18,
        label="Min-max corridor range",
    )
    ax.set_title("Jakarta Peak-Hour Corridor Speed by Month")
    ax.set_xlabel("Month in 2023")
    ax.set_ylabel("Speed (km/h)")
    ax.set_xticks(monthly["month"])
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=170)
    plt.close(fig)


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    speed = load_corridor_speed(RAW_SPEED_PATH)
    corridor_summary = summarize_corridors(speed)
    month_summary = monthly_summary(speed)

    speed.to_csv(PROCESSED_DIR / "jakarta_corridor_peak_speed_clean.csv", index=False)
    corridor_summary.to_csv(
        PROCESSED_DIR / "jakarta_corridor_bottleneck_ranking.csv",
        index=False,
    )
    month_summary.to_csv(
        PROCESSED_DIR / "jakarta_corridor_monthly_speed_summary.csv",
        index=False,
    )

    plot_slowest_corridors(
        corridor_summary,
        FIGURE_DIR / "jakarta_slowest_corridors.png",
    )
    plot_monthly_speed(
        month_summary,
        FIGURE_DIR / "jakarta_monthly_peak_speed.png",
    )

    print("Rows:", len(speed))
    print("Year(s):", ", ".join(map(str, sorted(speed["year"].unique()))))
    print("Corridors:", speed["corridor"].nunique())
    print("Slowest corridors:")
    print(corridor_summary.head(8).to_string(index=False))


if __name__ == "__main__":
    main()
