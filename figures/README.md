# Figure mapping

This directory contains public manuscript-supporting figures that can be regenerated from compact result tables.

## Existing public figures

- `main_curvature_migration_results.png` — public summary of the global and spatially varying curvature–migration results.
- `twoB_spatial_consistency.png` — public summary of spatial consistency at the 2B upstream spatial offset.

## Manuscript figure mapping

The manuscript uses a broader figure set than the public repository. The current robustness-stage mapping is:

- **Figure 1:** simplified geographic locator map of the tidal Rupsha–Pasur study corridor. This map should show regional setting and downstream orientation without analytical transects or block metadata.
- **Figures 2–7:** primary manuscript analytical figures; no robustness-driven redesign is required.
- **Figure S1:** uncertainty/resolvability diagnostic; unchanged.
- **Figure S2:** posterior computational diagnostics and divergence-sensitivity material; unchanged.
- **Figure S3:** post hoc robustness diagnostics, with four panels covering predictor dependence, posterior predictive fit, residual spatial dependence, and phase-balanced spatial thinning.

The intended final filename for the new supplementary robustness figure is:

`Figure_S03_posthoc_robustness_diagnostics_FINAL.png`

The exact numerical data underlying Figure S3 are provided in `results/`:

- `six_offset_predictor_pearson_correlation.csv`
- `six_offset_predictor_spearman_correlation.csv`
- `six_offset_global_beta_posterior_correlation.csv`
- `zero_nonzero_curvature_association_sensitivity.csv`
- `posterior_mean_residual_spatial_dependence.csv`
- `spatial_thinning_summary.csv`
- `robustness_diagnostics_summary.csv`

## Figure S3 caption

**Figure S3. Post hoc robustness diagnostics for the curvature–migration analysis.** (A) Pairwise Pearson correlations among the six width-normalized curvature predictors evaluated at upstream spatial offsets from 0B to 2.5B. (B) Empirical cumulative distributions of absolute standardized signed migration for the observed response and posterior predictive realizations from the fitted continuous Student-t likelihood. The posterior predictive distribution did not reproduce the large extraction-level exact-zero concentration or the full central response distribution, although the extreme upper tail was reproduced reasonably. (C) Posterior-mean residual correlation as a function of along-corridor station separation. Residual dependence was moderate at immediately adjacent stations but declined rapidly and approached zero over approximately 2.4–4.8 km. (D) Median descriptive Pearson curvature–migration correlations under phase-balanced spatial thinning from approximately 0.12 to 2.40 km station spacing. The negative relationship around 2B persisted as station density was progressively reduced. These diagnostics were conducted post hoc and did not alter the primary hierarchical Bayesian model or reported posterior estimates.

Publication-quality binary figure files should be exported from the original plotting environment rather than reconstructed from screenshots.