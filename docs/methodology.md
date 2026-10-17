# Methodology overview

## Study system

This project examines multi-decadal channel morphodynamics along
the tidal Rupsha–Pasur river corridor in southwest Bangladesh.

## Satellite-derived channel geometry

Annual channel geometry was reconstructed from Landsat imagery.
The workflow uses topology-aware water-channel extraction and a
fixed master river axis to maintain a consistent spatial
reference through time.

Derived geometry includes:

- bank positions
- channel center position
- channel width
- signed channel curvature
- lateral centerline migration

## Spatial reference framework

Channel geometry is referenced to fixed transects along a master
river axis.

The transverse coordinate is downstream referenced:

- positive transverse direction = river left looking downstream
- negative transverse direction = river right looking downstream

Signed center migration is calculated from changes in center
position between successive analysis periods.

## Curvature

The primary curvature predictor is signed, width-normalized
channel curvature derived using the W15 curvature scale.

Positive curvature represents a left-turning channel when
looking downstream.

## Upstream distributed lags

Curvature is evaluated at prespecified upstream spatial offsets:

- 0.0B
- 0.5B
- 1.0B
- 1.5B
- 2.0B
- 2.5B

where B is the channel width at the response station at the
start of the migration interval.

The target curvature position is defined as:

target position =
response position - lag × local channel width

The lag framework is spatial, not temporal.

## Inferential model

The final analysis uses a hierarchical Bayesian distributed-lag
model with a Student-t likelihood.

The model includes:

- corridor-wide lag coefficients
- block-specific lag deviations
- channel-width effect
- along-axis spatial structure
- station-level effects
- temporal-period effects
- block-period effects

The Student-t likelihood provides robustness to heavy-tailed
migration observations.

## Interpretation

Negative curvature coefficients correspond to migration in the
direction opposite to curvature sign and therefore to
outward-aligned migration under the locked coordinate
convention.

Positive coefficients correspond to inward-aligned migration.

The analysis evaluates statistical association. It does not, by
itself, establish causal effects or out-of-sample prediction
skill.

## Computational validation

The final working posterior contains 8,000 retained draws.

Two residual divergent transitions remained. Their influence was
audited explicitly. Sensitivity tests showed negligible effects
on both corridor-wide and block-specific scientific quantities.

The strict zero-divergence criterion therefore was not achieved,
but the posterior passed the predefined scientific sensitivity
checks used for interpretation.