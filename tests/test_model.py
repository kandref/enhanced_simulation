import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from traffic_fluid_model import TrafficParams, simulate


def test_simulation_shapes_and_bounds():
    params = TrafficParams(cells=40, total_time_s=5.0, dt_s=0.05)
    output = simulate(params)

    assert output.density.shape == (params.steps, params.cells)
    assert output.velocity_mps.shape == output.density.shape
    assert output.capacity.shape == output.density.shape
    assert np.isfinite(output.density).all()
    assert output.density.min() >= 0.0
    assert output.density.max() <= 0.99


def test_disturbance_reduces_capacity():
    params = TrafficParams(cells=40, disturbance_start_s=1.0, disturbance_end_s=3.0)
    output = simulate(params)

    before = abs(output.t_s - 0.0).argmin()
    during = abs(output.t_s - 2.0).argmin()
    assert output.capacity[during].min() < output.capacity[before].min()
