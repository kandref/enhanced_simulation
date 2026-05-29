from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from traffic_fluid_model import TrafficParams, simulate
from traffic_fluid_model.jakarta_data import (
    load_corridor_speed,
    monthly_summary,
    summarize_corridors,
)


st.set_page_config(page_title="Traffic Flow Simulation", layout="wide")
st.title("Traffic Flow Simulation")

simulation_tab, jakarta_tab = st.tabs(["Simulation", "Jakarta Data"])

with simulation_tab:
    with st.sidebar:
        st.header("Scenario")
        inflow_density = st.slider("Inflow density", 0.02, 0.90, 0.28, 0.01)
        bottleneck_strength = st.slider("Bottleneck strength", 0.0, 0.90, 0.35, 0.01)
        disturbance_strength = st.slider("Disturbance strength", 0.0, 0.90, 0.35, 0.01)
        disturbance_start_s = st.slider("Disturbance start (s)", 0.0, 80.0, 25.0, 1.0)
        disturbance_end_s = st.slider("Disturbance end (s)", 5.0, 90.0, 55.0, 1.0)
        vmax_kmh = st.slider("Free-flow speed (km/h)", 20.0, 120.0, 90.0, 5.0)

    if disturbance_end_s <= disturbance_start_s:
        disturbance_end_s = disturbance_start_s + 1.0

    params = TrafficParams(
        inflow_density=inflow_density,
        bottleneck_strength=bottleneck_strength,
        disturbance_strength=disturbance_strength,
        disturbance_start_s=disturbance_start_s,
        disturbance_end_s=disturbance_end_s,
        vmax_mps=vmax_kmh / 3.6,
    )
    output = simulate(params)

    mean_density = output.density.mean(axis=1)
    mean_speed_kmh = output.velocity_mps.mean(axis=1).mean() * 3.6
    peak_density = output.density.max()

    metric_cols = st.columns(3)
    metric_cols[0].metric("Mean density", f"{mean_density.mean():.3f}")
    metric_cols[1].metric("Peak density", f"{peak_density:.3f}")
    metric_cols[2].metric("Mean speed", f"{mean_speed_kmh:.1f} km/h")

    heatmap = go.Figure(
        data=go.Heatmap(
            z=output.density,
            x=output.x_m,
            y=output.t_s,
            colorscale="Viridis",
            zmin=0,
            zmax=1,
            colorbar={"title": "Density"},
        )
    )
    heatmap.update_layout(
        title="Density Heatmap",
        xaxis_title="Road position (m)",
        yaxis_title="Time (s)",
        height=480,
        margin={"l": 20, "r": 20, "t": 50, "b": 20},
    )
    st.plotly_chart(heatmap, use_container_width=True)

    snapshot_times = [0, 20, 40, 70, 90]
    snapshot = go.Figure()
    for time_s in snapshot_times:
        idx = abs(output.t_s - time_s).argmin()
        snapshot.add_trace(
            go.Scatter(
                x=output.x_m,
                y=output.density[idx],
                mode="lines",
                name=f"{output.t_s[idx]:.0f}s",
            )
        )
    snapshot.update_layout(
        title="Density Snapshots",
        xaxis_title="Road position (m)",
        yaxis_title="Normalized density",
        yaxis_range=[0, 1],
        height=420,
        margin={"l": 20, "r": 20, "t": 50, "b": 20},
    )
    st.plotly_chart(snapshot, use_container_width=True)


@st.cache_data
def load_jakarta_outputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    raw_path = ROOT / "data" / "raw" / "jakarta_41_corridor_peak_speed.csv"
    speed = load_corridor_speed(raw_path)
    return speed, summarize_corridors(speed), monthly_summary(speed)


with jakarta_tab:
    speed, corridor_summary, month_summary = load_jakarta_outputs()

    jakarta_metrics = st.columns(4)
    jakarta_metrics[0].metric("Rows", f"{len(speed):,}")
    jakarta_metrics[1].metric("Year", ", ".join(map(str, sorted(speed["year"].unique()))))
    jakarta_metrics[2].metric("Corridors", f"{speed['corridor'].nunique()}")
    jakarta_metrics[3].metric("Mean speed", f"{speed['speed_kmh'].mean():.1f} km/h")

    slowest = corridor_summary.head(15).sort_values("mean_speed_kmh")
    slowest_chart = go.Figure(
        data=go.Bar(
            x=slowest["mean_speed_kmh"],
            y=slowest["corridor"],
            orientation="h",
            marker_color="#c23b22",
        )
    )
    slowest_chart.update_layout(
        title="Slowest Peak-Hour Corridors",
        xaxis_title="Mean speed (km/h)",
        yaxis_title="Corridor",
        height=560,
        margin={"l": 20, "r": 20, "t": 50, "b": 20},
    )
    st.plotly_chart(slowest_chart, use_container_width=True)

    monthly_chart = go.Figure()
    monthly_chart.add_trace(
        go.Scatter(
            x=month_summary["month"],
            y=month_summary["mean_speed_kmh"],
            mode="lines+markers",
            name="Mean",
        )
    )
    monthly_chart.add_trace(
        go.Scatter(
            x=month_summary["month"],
            y=month_summary["min_speed_kmh"],
            mode="lines",
            name="Min",
            line={"dash": "dot"},
        )
    )
    monthly_chart.add_trace(
        go.Scatter(
            x=month_summary["month"],
            y=month_summary["max_speed_kmh"],
            mode="lines",
            name="Max",
            line={"dash": "dot"},
        )
    )
    monthly_chart.update_layout(
        title="Monthly Peak-Hour Corridor Speed",
        xaxis_title="Month in 2023",
        yaxis_title="Speed (km/h)",
        height=430,
        margin={"l": 20, "r": 20, "t": 50, "b": 20},
    )
    st.plotly_chart(monthly_chart, use_container_width=True)

    st.dataframe(corridor_summary, use_container_width=True, hide_index=True)
