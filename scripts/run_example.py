from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from traffic_fluid_model import TrafficParams, simulate
from traffic_fluid_model.visualization import (
    plot_density_heatmap,
    plot_density_snapshots,
    plot_summary,
    save_density_animation,
)


def main() -> None:
    output_dir = ROOT / "results" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)

    params = TrafficParams()
    output = simulate(params)

    plot_density_heatmap(output, output_dir / "density_heatmap.png")
    plot_density_snapshots(output, output_dir / "density_snapshots.png")
    plot_summary(output, output_dir / "summary.png")

    try:
        save_density_animation(output, output_dir / "density_animation.gif")
    except Exception as exc:
        print(f"Animation skipped: {exc}")

    print(f"Saved outputs to {output_dir}")


if __name__ == "__main__":
    main()
