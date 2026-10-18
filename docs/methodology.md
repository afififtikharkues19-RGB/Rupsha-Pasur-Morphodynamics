# Methodology overview

## Study system

This project examines multi-decadal channel morphodynamics along the tidal Rupsha–Pasur river corridor in southwest Bangladesh using 35 analysis years spanning 1988–2025. Annual states are not uninterrupted; 2007, 2011, and 2012 are absent from the analysis record.

## Satellite-derived channel geometry

Landsat observations were processed using adaptive MNDWI thresholding with row-specific Otsu classification and topology-connected reconstruction of the main channel.

The mapped channel margins are interpreted as **satellite-observed outer water–land boundary proxies**, not surveyed geomorphic banks.

A fixed master river axis and transect framework provide a consistent spatial reference through time. Derived geometry includes:

- satellite-observed outer water–land boundary-proxy positions;
- mapped center position;
- channel width;
- signed channel curvature; and
- continuous signed mapped-centerline migration.

The production geometry contains 1,048 transects over approximately 126 km. The inferential common-support dataset contains 1,014 stations spanning approximately 121.6 km.

## Spatial reference framework

The transverse coordinate is downstream referenced:

- positive transverse direction = river left looking downstream;
- negative transverse direction = river right looking downstream.

Let `n_R` and `n_L` denote the right and left boundary positions on a transect. Channel width is `B = n_L − n_R`, and mapped-center position is `n_C = (n_L + n_R)/2`.

Signed mapped-centerline migration between two analysis states is derived from the change in `n_C` divided by elapsed time. Positive migration is toward river left and negative migration toward river right under this coordinate convention.

## Curvature and width normalization

The primary curvature predictor is signed W15 curvature, where positive curvature denotes a left-turning channel when looking downstream. The primary width-normalized predictor is `κB = κ × B`.

## Upstream spatial offsets

Curvature is evaluated at six prespecified upstream spatial offsets:

- 0B
- 0.5B
- 1B
- 1.5B
- 2B
- 2.5B

For station `i`, start state `t1`, and dimensionless offset multiplier `λ`, the target position is:

`target position = s_i − λ B_i,t1`

where `B_i,t1` is the start-state local width at the response station. Predictor values at target positions are obtained by linear interpolation between adjacent stations.

These are **upstream spatial offsets**, not temporal lags. The model implementation retains distributed-lag parameter names, but scientific interpretation uses spatial-offset terminology.

## Inferential dataset

The final common-support inferential dataset contains:

- 25,923 observations;
- 1,014 unique stations;
- 34 migration periods;
- 12 spatial blocks; and
- 365 observed block-period combinations.

The response is continuous signed mapped-centerline migration rate. Exact zeros are retained as extracted values and are not recoded as statistically undetected movement.

## Inferential model

The final analysis uses a hierarchical Bayesian model with a continuous Student-t likelihood. The mean structure includes:

- six corridor-wide curvature coefficients at the tested spatial offsets;
- mean-centered block-specific deviations for the six curvature coefficients;
- standardized log-width;
- eight standardized along-axis spline bases;
- station effects;
- temporal-period effects; and
- block-period effects.

The six global curvature coefficients are regularized using a first-order random-walk prior across adjacent tested offsets. Block-specific deviations are mean-centered across blocks so the global coefficients retain their corridor-wide interpretation.

The model is inferential rather than predictive; no out-of-sample prediction claim is made.

## Measurement uncertainty

Migration remains continuous in the primary analysis; no threshold censoring or binary detection model is used.

Empirical temporal centerline-error distributions are used to characterize displacement resolvability. A converged 2,000-realization joint geometry ensemble separately propagates geometry uncertainty through migration and W15 curvature recomputation.

The primary Bayesian posterior is a **nominal-geometry posterior**. Measurement error is not explicitly integrated into the likelihood, and the 2,000 geometry realizations are not pooled as separate posterior fits.

## Posterior computation

The final retained posterior contains 8,000 draws from four chains after 1,500 tuning iterations and 2,000 retained draws per chain, using a target acceptance rate of 0.995.

Two divergent transitions remained among the 8,000 retained draws (0.025%), with no maximum tree-depth hits. The strict zero-divergence computational gate therefore failed. A dedicated sensitivity audit removing the divergent draws produced negligible changes in the global scientific quantities and no change in 95% interval classification, so the scientific robustness gate passed and no further sampling was performed.

## Post hoc robustness diagnostics

After the primary inferential analysis was frozen, additional diagnostics were conducted without refitting or resampling the production model. These included:

- Pearson and Spearman correlations among the six curvature predictors;
- posterior correlations among the six global curvature coefficients;
- descriptive curvature–migration correlations for all observations versus nonzero extracted displacements;
- posterior predictive simulation from the fitted continuous Student-t likelihood;
- posterior-mean residual correlation across increasing within-period station separations; and
- phase-balanced spatial thinning from approximately 0.12 to 2.40 km station spacing.

These diagnostics assess sensitivity and model adequacy but do not replace the primary hierarchical posterior.

## Interpretation

A negative global curvature coefficient indicates an opposite-signed curvature–migration relationship. Under the locked downstream-referenced sign convention, this corresponds to an **outward-aligned** tendency. Positive coefficients correspond to inward-aligned relationships.

The analysis evaluates conditional association. It does not establish causation, identify a universal physical optimum at exactly 2B, or demonstrate out-of-sample prediction skill.