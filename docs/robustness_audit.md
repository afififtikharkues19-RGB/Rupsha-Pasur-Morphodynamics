# Post hoc robustness audit

## Scope

These diagnostics were conducted after the primary inferential model and scientific decisions were frozen. They are **diagnostic-only** checks: the production Bayesian model was not redesigned, refitted, or resampled.

The audit addresses four reviewer-facing concerns:

1. dependence among the six upstream curvature predictors;
2. posterior coefficient trade-off across spatial offsets;
3. sensitivity of the curvature–migration pattern to the large exact-zero response concentration; and
4. residual short-range spatial dependence and dense station sampling.

A posterior predictive check was also used to assess the marginal response distribution under the fitted continuous Student-t likelihood.

## 1. Predictor dependence

For the six width-normalized curvature predictors (0B, 0.5B, 1B, 1.5B, 2B, 2.5B), the maximum off-diagonal Pearson correlation was **0.296**, indicating weak linear dependence. Neighboring offsets retained moderate rank continuity, with a maximum Spearman correlation of **0.571**.

This pattern is consistent with spatially related but not linearly redundant predictors.

## 2. Posterior coefficient dependence

Posterior correlations among the six global curvature coefficients were modest. The maximum absolute off-diagonal posterior correlation was **0.301** (0B versus 2B).

No severe posterior coefficient competition was evident.

## 3. Exact-zero sensitivity

The inferential response contains **25,923** observations:

- exact-zero extracted mapped-centerline displacement: **14,545 (56.1%)**;
- nonzero extracted displacement: **11,378 (43.9%)**.

At 2B, descriptive curvature–migration correlations were:

| Sample | Pearson | Spearman |
|---|---:|---:|
| All observations | −0.0492 | −0.0621 |
| Nonzero extracted displacements only | −0.0724 | −0.0920 |

The negative descriptive relationship therefore did not disappear after exact-zero observations were excluded; it strengthened.

These descriptive correlations are not substitutes for the hierarchical posterior. They are sensitivity diagnostics only.

## 4. Posterior predictive check

Posterior predictive simulations were reconstructed from the retained production posterior without refitting the model. The Student-t residual scale and degrees of freedom had posterior medians of approximately **σ = 0.3253** and **ν = 2.0004**.

The continuous likelihood did not reproduce the large extraction-level point mass at the standardized zero-displacement value (observed modal fraction **0.5611**). It also did not fully reproduce the central response distribution: observed median absolute standardized response, P75, and P95 fell outside the corresponding 95% posterior predictive intervals.

The observed P99 absolute standardized response (**3.0522**) was inside the 95% posterior predictive interval (**3.0396–3.4537**).

Accordingly, the marginal posterior predictive assessment is treated as an **important model-fit limitation**, not as a full pass. In particular, the continuous Student-t likelihood cannot represent a discrete extraction-level zero mass.

## 5. Residual spatial dependence

Posterior-mean residual correlation was evaluated within migration periods at increasing station separations.

| Approx. separation (km) | Residual correlation |
|---:|---:|
| 0.12 | 0.2719 |
| 0.24 | 0.2211 |
| 0.60 | 0.1517 |
| 1.20 | 0.0902 |
| 2.40 | 0.0263 |
| 4.80 | −0.0036 |

Residual dependence is therefore moderate at immediately adjacent stations but declines rapidly and approaches zero over approximately 2.4–4.8 km.

Across 34 migration periods, adjacent-station residual correlation had median **0.2354**, mean **0.2449**, minimum **0.0416**, and maximum **0.5932**. Higher adjacent residual correlation tended to coincide with lower exact-zero fractions and larger migration magnitudes, indicating period-varying short-range spatial coherence.

## 6. Phase-balanced spatial thinning

To assess whether dense ~120 m station spacing generated the descriptive curvature–migration profile, stations were progressively thinned to approximately 0.24, 0.60, 1.20, and 2.40 km spacing. All possible starting phases were evaluated for each thinning interval.

Median 2B correlations remained stable:

| Approx. spacing (km) | Median Pearson at 2B | Median Spearman at 2B |
|---:|---:|---:|
| 0.12 | −0.0492 | −0.0621 |
| 0.24 | −0.0493 | −0.0621 |
| 0.60 | −0.0473 | −0.0640 |
| 1.20 | −0.0519 | −0.0643 |
| 2.40 | −0.0507 | −0.0710 |

At the coarsest ~2.40 km spacing, 2B remained negative across every tested phase:

- Pearson range: **−0.1035 to −0.0147**;
- Spearman range: **−0.1006 to −0.0329**.

This reduces concern that the negative 2B descriptive relationship is an artifact of dense local station sampling.

## Interpretation

The audit supports the following conclusions:

- severe predictor collinearity was not detected;
- severe posterior coefficient trade-off was not detected;
- the negative 2B descriptive relationship was not created by exact-zero observations;
- short-range residual spatial dependence remains, but decays rapidly with separation;
- the negative 2B descriptive relationship persists under strong phase-balanced spatial thinning; and
- the continuous Student-t likelihood does not reproduce the full marginal response distribution, especially the large exact-zero concentration.

These diagnostics do not change the primary posterior estimates. They strengthen the interpretation that the corridor-wide 2B association is directionally robust while preserving explicit limitations concerning marginal response fit and local residual spatial dependence.