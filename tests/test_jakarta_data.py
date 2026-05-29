import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from traffic_fluid_model.jakarta_data import load_corridor_speed, summarize_corridors


def test_corridor_speed_loader_parses_decimal_comma():
    speed = load_corridor_speed(ROOT / "data" / "raw" / "jakarta_41_corridor_peak_speed.csv")

    assert len(speed) == 576
    assert speed["year"].nunique() == 1
    assert speed["year"].iloc[0] == 2023
    assert speed["speed_kmh"].dtype.kind == "f"
    assert speed["corridor"].nunique() == 48


def test_corridor_summary_ranks_slowest_first():
    speed = load_corridor_speed(ROOT / "data" / "raw" / "jakarta_41_corridor_peak_speed.csv")
    summary = summarize_corridors(speed)

    assert summary.iloc[0]["bottleneck_rank"] == 1
    assert summary["mean_speed_kmh"].is_monotonic_increasing
