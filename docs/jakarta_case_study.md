# Jakarta Case Study

This note reframes the thesis-inspired simulation into a Jakarta congestion case
study. The goal is not to claim a full Navier-Stokes traffic solver. The goal is
to explain why congestion can emerge using a defensible macroscopic traffic-flow
story: demand, capacity, speed reduction, bottlenecks, and density waves.

## Research Question

Why can congestion persist in Jakarta even when traffic policies and public
transport improvements exist?

## Working Explanation

Jakarta congestion can be treated as a demand-capacity imbalance:

1. Vehicle ownership creates high demand for road space.
2. Road capacity and effective corridor capacity are limited.
3. During peak periods, density rises on major corridors.
4. Higher density reduces average speed.
5. Local capacity reductions create bottlenecks.
6. Bottlenecks generate queue-like density waves that propagate upstream.

This explanation connects naturally to a one-dimensional conservation-law model:

```text
density_t + flux(density)_x = 0
```

with a speed-density relationship:

```text
velocity = vmax * capacity(x, t) * (1 - density)
flux = density * velocity
```

## Data Sources To Use

### Vehicle Demand

- BPS DKI Jakarta: registered motor vehicles by municipality and vehicle type,
  2024.
- BPS Indonesia: Land Transportation Statistics 2024, including road and vehicle
  statistics.

Use this layer to describe structural demand pressure.

### Corridor Speed

- Satu Data Indonesia/Jakarta: average speed on 41 main road corridors during
  peak hours.

Use this layer to identify slow corridors and infer bottleneck intensity.

### Corridor Traffic Example

- Mendeley Data: Traffic and Emission data, Thamrin Jakarta. The dataset was
  published on 10 December 2024 as version 2 and is licensed CC BY 4.0.

Use this as a corridor-level example if the file contains usable time-series
traffic variables.

### External Congestion Context

- TomTom Traffic Index: Jakarta city profile and Indonesia ranking.

Use this only as context, not as the calibration source for the simulation.

## Analysis Pipeline

1. Collect and archive source metadata.
2. Convert usable data into CSV under `data/raw`.
3. Build `notebooks/01_jakarta_data_exploration.ipynb`.
4. Plot vehicle growth, corridor speed distribution, and peak-hour speed ranks.
5. Select one or more corridors for simulation scenarios.
6. Calibrate simple parameters such as `vmax`, bottleneck strength, and
   disturbance duration.
7. Compare simulated speed/density patterns against the observed corridor data.

## Boundary Of The Claim

The final claim should be modest:

> This project modernizes a thesis prototype into a reproducible Python
> workflow for exploring Jakarta traffic congestion using macroscopic
> fluid-inspired traffic-flow simulation.

Avoid claiming:

- a full Navier-Stokes implementation
- a calibrated city-wide Jakarta traffic model
- a policy recommendation without validation

## Source Links

- BPS DKI Jakarta vehicle data:
  https://jakarta.bps.go.id/id/statistics-table/3/VjJ3NGRGa3dkRk5MTlU1bVNFOTVVbmQyVURSTVFUMDkjMw%3D%3D/number-of-registered-motor-vehicles-by-regency-municipality-and-type-of-motor-vehicles-in-dki-jakarta-province--units---2021.html
- BPS Land Transportation Statistics 2024:
  https://www.bps.go.id/id/publication/2025/12/01/ed7ff73d58fc0719ee3df145/land-transportation-statistics-2024.html
- Satu Data corridor speed dataset:
  https://fe-staging.data.go.id/dataset/dataset/kecepatan-rata-rata-di-41-empat-puluh-satu-koridor-jalan-utama-pada-jam-sibuk
- Mendeley Thamrin traffic/emission data:
  https://data.mendeley.com/datasets/nf3gds4zk9/2
- TomTom Jakarta Traffic Index:
  https://www.tomtom.com/traffic-index/city/jakarta
