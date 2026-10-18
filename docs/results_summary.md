# Core inferential results

## Corridor-wide curvature–migration response

Among the six tested upstream spatial offsets, the clearest corridor-wide curvature–migration association occurred at **2B upstream**.

The standardized global coefficient at 2B was **−0.005916** (95% CrI **−0.012488 to −0.001293**; P[β < 0] = **0.993375**).

On the physical response scale, this corresponds to **−0.085 m yr⁻¹ per +1 SD κB** (95% CrI **−0.180 to −0.019 m yr⁻¹**).

Under the locked downstream-referenced sign convention, this negative coefficient represents an opposite-signed curvature–migration relationship and therefore an **outward-aligned tendency**.

The corridor-wide magnitude is small: the standardized 2B effect is approximately 0.59% of one response standard deviation per +1 SD κB.

## Global offset profile

The six global curvature coefficients are:

| Offset | Posterior mean | 95% CrI | P(β < 0) | Physical effect (m yr⁻¹ per +1 SD κB) |
|---|---:|---:|---:|---:|
| 0B | +0.001722 | −0.004454 to +0.009717 | 0.358 | +0.025 |
| 0.5B | −0.002575 | −0.008474 to +0.002758 | 0.843 | −0.037 |
| 1B | −0.003471 | −0.009016 to +0.001662 | 0.921 | −0.050 |
| 1.5B | −0.003932 | −0.009608 to +0.001652 | 0.934 | −0.057 |
| 2B | **−0.005916** | **−0.012488 to −0.001293** | **0.993** | **−0.085** |
| 2.5B | −0.003558 | −0.009138 to +0.002691 | 0.891 | −0.051 |

Only 2B has a global 95% credible interval fully below zero. This does not establish 2B as a universal physical optimum; it is the clearest association among the six tested offsets.

## Spatial consistency at 2B

At 2B, **10 of 12** block posterior means are negative and 2 are positive.

- 3 of 12 blocks have P(outward) ≥ 0.90;
- 1 of 12 has P(outward) ≥ 0.95;
- 0 of 12 has a fully negative local 95% credible interval.

The 2B result is therefore interpreted as a **spatially widespread directional tendency with substantial local uncertainty**, not as a uniformly resolved block-level effect.

## Locally resolved heterogeneity

Across the full 0–2.5B spatial-offset domain, four block-by-offset effects have 95% credible intervals excluding zero:

- **B07 at 1.5B:** inward-aligned, +0.397 m yr⁻¹ per +1 SD κB (95% CrI 0.176 to 0.638);
- **B09 at 2.5B:** outward-aligned, −0.301 m yr⁻¹ (95% CrI −0.601 to −0.034);
- **B10 at 0.5B:** outward-aligned, −0.151 m yr⁻¹ (95% CrI −0.262 to −0.046);
- **B10 at 1B:** outward-aligned, −0.130 m yr⁻¹ (95% CrI −0.237 to −0.025).

These local effects show that the magnitude, direction, and apparent spatial offset of curvature–migration coupling vary along the corridor.

## Response structure

The inferential response contains 25,923 observations. Of these, **14,545 (56.1%)** are exact zero extracted mapped-centerline displacements and **11,378 (43.9%)** are nonzero extracted displacements.

The primary analysis retains this continuous signed response without threshold censoring or a binary movement model.

## Post hoc robustness audit

The primary scientific pattern remained stable across several no-refit diagnostics:

- maximum pairwise predictor Pearson correlation = **0.296**;
- maximum pairwise predictor Spearman correlation = **0.571**;
- maximum absolute posterior correlation among global curvature coefficients = **0.301**;
- at 2B, Pearson correlation strengthened from **−0.0492** in all observations to **−0.0724** among nonzero extracted displacements;
- at 2B, Spearman correlation strengthened from **−0.0621** to **−0.0920** among nonzero observations;
- posterior-mean residual correlation declined from **0.272 at ~0.12 km** to **0.090 at ~1.2 km**, **0.026 at ~2.4 km**, and approximately zero by **~4.8 km**;
- phase-balanced spatial thinning preserved a negative 2B descriptive association through approximately **2.4 km** station spacing.

The posterior predictive check identified a real likelihood limitation: the continuous Student-t likelihood does **not** reproduce the extraction-level exact-zero point mass or the full central response distribution. The observed P99 absolute response was, however, inside the 95% posterior predictive interval. This model-fit limitation is reported explicitly rather than treated as evidence of full marginal-distribution adequacy.

## Computational sensitivity

Two NUTS divergences remained among 8,000 retained draws. Removing the two divergent draws changed global standardized posterior means by at most approximately 0.000344 posterior SD and changed sign probabilities by at most approximately 0.000108. No global 95% interval classification changed.

The strict zero-divergence computational criterion therefore failed, while the scientific sensitivity assessment passed.

## Claim boundary

The analysis supports a conditional association between antecedent channel geometry and subsequent signed mapped-centerline migration. It does not establish causation, prove a universal optimum at exactly 2B, or demonstrate out-of-sample predictive skill. The mapped channel margins are satellite-observed outer water–land boundary proxies rather than surveyed geomorphic banks.