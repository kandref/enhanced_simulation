# Enhanced Simulation

An enhanced Python traffic-flow simulation inspired by a thesis prototype that
modelled road traffic using simplified fluid dynamics. The current enhancement
direction uses Jakarta as the practical case-study context.

The original thesis PDF is not included. This repository focuses on extending
the appendix prototype into a reproducible Python project with a modular solver,
static plots, animation support, and an interactive Streamlit dashboard.

## Project Framing

The companion repository `original_reproduction` keeps a close translation of
the Scilab appendix. This repository is the enhancement layer:

- a one-dimensional road model for normalized traffic density
- Greenshields-style velocity-density relation
- finite-volume update for conservation-law dynamics
- bottleneck and time-window disturbance parameters
- static heatmap and snapshot plots
- optional animated density evolution
- Streamlit dashboard for parameter exploration

## Jakarta Case Study Direction

The Jakarta extension focuses on explaining congestion as a demand-capacity
problem:

```text
vehicle demand grows
        ->
road and corridor capacity is limited
        ->
peak-hour density increases
        ->
average speed drops
        ->
bottlenecks and queue-like density waves appear
```

The planned data layer combines:

- BPS DKI Jakarta vehicle registration statistics
- Satu Data Indonesia/Jakarta corridor-speed datasets
- Thamrin traffic and emission dataset on Mendeley Data
- TomTom Traffic Index as external congestion context

See `docs/jakarta_case_study.md` and `data/README.md`.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Generate Example Outputs

```bash
python scripts/run_example.py
```

Figures are written to:

```text
results/figures/
```

## Run Dashboard

```bash
streamlit run app.py
```

## Model Summary

The simulation treats traffic density like a conserved quantity moving along a
one-dimensional road:

```text
density_t + flux(density)_x = 0
```

The flux uses a simplified velocity-density relationship:

```text
velocity = vmax * capacity(x, t) * (1 - density)
flux = density * velocity
```

`capacity(x, t)` is reduced near bottlenecks or during disturbances. This keeps
the project connected to the thesis idea while making the simulation easier to
extend and visualize.
