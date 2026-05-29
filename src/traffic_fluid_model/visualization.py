from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from .model import SimulationOutput


def plot_density_heatmap(output: SimulationOutput, path: str | Path | None = None):
    fig, ax = plt.subplots(figsize=(9, 5))
    image = ax.imshow(
        output.density,
        origin="lower",
        aspect="auto",
        extent=[
            output.x_m[0],
            output.x_m[-1],
            output.t_s[0],
            output.t_s[-1],
        ],
        cmap="viridis",
        vmin=0,
        vmax=1,
    )
    fig.colorbar(image, ax=ax, label="Normalized density")
    ax.set_title("Traffic Density Over Time")
    ax.set_xlabel("Road position (m)")
    ax.set_ylabel("Time (s)")
    fig.tight_layout()
    if path:
        fig.savefig(path, dpi=170)
    return fig


def plot_density_snapshots(
    output: SimulationOutput,
    path: str | Path | None = None,
    times_s: tuple[float, ...] = (0, 20, 40, 70, 90),
):
    fig, ax = plt.subplots(figsize=(9, 4.8))
    for time_s in times_s:
        idx = abs(output.t_s - time_s).argmin()
        ax.plot(output.x_m, output.density[idx], label=f"{output.t_s[idx]:.0f}s")
    ax.set_title("Density Snapshots")
    ax.set_xlabel("Road position (m)")
    ax.set_ylabel("Normalized density")
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3)
    ax.legend(title="Time")
    fig.tight_layout()
    if path:
        fig.savefig(path, dpi=170)
    return fig


def plot_summary(output: SimulationOutput, path: str | Path | None = None):
    mean_density = output.density.mean(axis=1)
    mean_speed_kmh = output.velocity_mps.mean(axis=1) * 3.6

    fig, ax_density = plt.subplots(figsize=(9, 4.8))
    ax_speed = ax_density.twinx()
    ax_density.plot(output.t_s, mean_density, color="tab:blue", label="Density")
    ax_speed.plot(output.t_s, mean_speed_kmh, color="tab:red", label="Speed")
    ax_density.set_title("Network-Level Summary")
    ax_density.set_xlabel("Time (s)")
    ax_density.set_ylabel("Mean normalized density")
    ax_speed.set_ylabel("Mean speed (km/h)")
    ax_density.grid(True, alpha=0.3)

    lines = ax_density.get_lines() + ax_speed.get_lines()
    ax_density.legend(lines, [line.get_label() for line in lines])
    fig.tight_layout()
    if path:
        fig.savefig(path, dpi=170)
    return fig


def save_density_animation(
    output: SimulationOutput,
    path: str | Path,
    every: int = 8,
    fps: int = 18,
) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.5))
    (line,) = ax.plot([], [], color="tab:blue")
    ax.set_xlim(output.x_m[0], output.x_m[-1])
    ax.set_ylim(0, 1)
    ax.set_xlabel("Road position (m)")
    ax.set_ylabel("Normalized density")
    ax.grid(True, alpha=0.3)

    frame_indices = list(range(0, len(output.t_s), every))

    def update(frame_idx: int):
        idx = frame_indices[frame_idx]
        line.set_data(output.x_m, output.density[idx])
        ax.set_title(f"Traffic Density Evolution | t = {output.t_s[idx]:.1f}s")
        return (line,)

    animation = FuncAnimation(fig, update, frames=len(frame_indices), blit=False)
    animation.save(path, writer=PillowWriter(fps=fps))
    plt.close(fig)
