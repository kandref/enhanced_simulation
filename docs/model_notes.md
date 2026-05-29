# Model Notes

This repository intentionally moves beyond the appendix scripts while keeping
the same thesis idea: traffic can be treated as a simplified fluid-like flow.

## Conservation Form

The core equation is a one-dimensional conservation law:

```text
density_t + flux(density)_x = 0
```

Density is normalized from `0` to `1`, where `1` represents a jammed road.

## Velocity-Density Relation

The model uses a Greenshields-style relation:

```text
velocity = vmax * capacity(x, t) * (1 - density)
```

As density increases, velocity decreases. Local capacity reductions represent
bottlenecks and temporary disturbances.

## Numerical Method

The update uses a finite-volume Rusanov flux. This is more robust than directly
differencing the conservation equation and is a reasonable next step from the
thesis prototype for a portfolio project.

## Enhancement Boundary

This is not a calibrated transport-engineering model. It is a reproducible
simulation prototype that makes the original mathematical idea easier to inspect,
run, and extend.
