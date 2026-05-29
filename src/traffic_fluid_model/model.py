from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class TrafficParams:
    road_length_m: float = 1000.0
    cells: int = 160
    total_time_s: float = 90.0
    dt_s: float = 0.10
    vmax_mps: float = 25.0
    inflow_density: float = 0.28
    outflow_density: float = 0.16
    initial_peak_density: float = 0.58
    initial_peak_center_m: float = 260.0
    initial_peak_width_m: float = 90.0
    bottleneck_center_m: float = 620.0
    bottleneck_width_m: float = 80.0
    bottleneck_strength: float = 0.35
    disturbance_start_s: float = 25.0
    disturbance_end_s: float = 55.0
    disturbance_center_m: float = 700.0
    disturbance_width_m: float = 110.0
    disturbance_strength: float = 0.35

    @property
    def dx_m(self) -> float:
        return self.road_length_m / self.cells

    @property
    def steps(self) -> int:
        return int(round(self.total_time_s / self.dt_s)) + 1


@dataclass(frozen=True)
class SimulationOutput:
    params: TrafficParams
    t_s: np.ndarray
    x_m: np.ndarray
    density: np.ndarray
    velocity_mps: np.ndarray
    capacity: np.ndarray


def gaussian(x: np.ndarray, center: float, width: float) -> np.ndarray:
    width = max(width, 1e-9)
    return np.exp(-((x - center) ** 2) / (2 * width**2))


def initial_density(params: TrafficParams, x_m: np.ndarray) -> np.ndarray:
    peak = params.initial_peak_density * gaussian(
        x_m,
        params.initial_peak_center_m,
        params.initial_peak_width_m,
    )
    base = params.inflow_density * np.ones_like(x_m)
    return np.clip(base + peak, 0.0, 0.98)


def capacity_profile(params: TrafficParams, x_m: np.ndarray, time_s: float) -> np.ndarray:
    bottleneck = params.bottleneck_strength * gaussian(
        x_m,
        params.bottleneck_center_m,
        params.bottleneck_width_m,
    )
    active_disturbance = params.disturbance_start_s <= time_s <= params.disturbance_end_s
    disturbance_scale = params.disturbance_strength if active_disturbance else 0.0
    disturbance = disturbance_scale * gaussian(
        x_m,
        params.disturbance_center_m,
        params.disturbance_width_m,
    )
    return np.clip(1.0 - bottleneck - disturbance, 0.05, 1.0)


def flux(params: TrafficParams, density: np.ndarray, capacity: np.ndarray) -> np.ndarray:
    velocity = params.vmax_mps * capacity * (1.0 - density)
    return density * velocity


def rusanov_step(
    params: TrafficParams,
    density: np.ndarray,
    capacity: np.ndarray,
) -> np.ndarray:
    left_boundary = np.array([params.inflow_density])
    right_boundary = np.array([params.outflow_density])
    rho_ext = np.concatenate([left_boundary, density, right_boundary])
    cap_ext = np.concatenate([capacity[:1], capacity, capacity[-1:]])

    rho_left = rho_ext[:-1]
    rho_right = rho_ext[1:]
    cap_face = 0.5 * (cap_ext[:-1] + cap_ext[1:])

    flux_left = flux(params, rho_left, cap_face)
    flux_right = flux(params, rho_right, cap_face)
    max_wave_speed = params.vmax_mps
    face_flux = 0.5 * (flux_left + flux_right) - 0.5 * max_wave_speed * (
        rho_right - rho_left
    )

    next_density = density - (params.dt_s / params.dx_m) * (
        face_flux[1:] - face_flux[:-1]
    )
    return np.clip(next_density, 0.0, 0.99)


def simulate(params: TrafficParams | None = None) -> SimulationOutput:
    params = params or TrafficParams()
    if params.dt_s > params.dx_m / params.vmax_mps:
        raise ValueError(
            "dt_s is too large for the default CFL safety check; reduce dt_s or cells."
        )

    x_m = (np.arange(params.cells) + 0.5) * params.dx_m
    t_s = np.linspace(0.0, params.total_time_s, params.steps)
    density = np.zeros((params.steps, params.cells), dtype=float)
    capacity = np.zeros_like(density)
    velocity = np.zeros_like(density)

    density[0] = initial_density(params, x_m)
    capacity[0] = capacity_profile(params, x_m, t_s[0])
    velocity[0] = params.vmax_mps * capacity[0] * (1.0 - density[0])

    for step in range(1, params.steps):
        previous_time = t_s[step - 1]
        previous_capacity = capacity_profile(params, x_m, previous_time)
        density[step] = rusanov_step(params, density[step - 1], previous_capacity)
        capacity[step] = capacity_profile(params, x_m, t_s[step])
        velocity[step] = params.vmax_mps * capacity[step] * (1.0 - density[step])

    return SimulationOutput(
        params=params,
        t_s=t_s,
        x_m=x_m,
        density=density,
        velocity_mps=velocity,
        capacity=capacity,
    )
