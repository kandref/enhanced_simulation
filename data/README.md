# Data Plan

The repository currently includes source metadata and an analysis plan, not raw
Jakarta datasets. Raw files should be added only when their license and format
are clear.

## Candidate Sources

| Layer | Source | Status | Intended Use |
| --- | --- | --- | --- |
| Vehicle demand | BPS DKI Jakarta registered vehicles by city and type, 2024 | Identified | Demand pressure and vehicle composition |
| Road context | BPS Land Transportation Statistics 2024 | Identified | Road length and transport context |
| Corridor speed | Satu Data/Jakarta 41 peak-hour corridors | Identified | Bottleneck and speed ranking |
| Corridor example | Mendeley Thamrin traffic and emission data | Identified | Corridor-level traffic example |
| Global context | TomTom Traffic Index Jakarta | Identified | External congestion benchmark |

## Proposed Local Layout

```text
data/
  raw/
    bps_dki_registered_vehicles_2024.csv
    jakarta_41_corridor_peak_speed.csv
    thamrin_traffic_emission_2024/
  processed/
    jakarta_corridor_speed_clean.csv
    jakarta_vehicle_pressure_summary.csv
```

## Minimum Fields Needed

For vehicle demand:

```text
year, area, motorcycles, passenger_cars, buses, trucks, total
```

For corridor speed:

```text
year, corridor, direction, period, speed_kmh
```

For time-series traffic data:

```text
timestamp, location, direction, vehicle_count, speed_kmh
```

## Notes

- BPS and Satu Data should be preferred for official Jakarta context.
- TomTom is useful for city-level context but should not be treated as the main
  calibration source unless the needed raw variables are available.
- The Mendeley dataset is licensed CC BY 4.0, but the actual files still need to
  be inspected before adding them to the repository.
