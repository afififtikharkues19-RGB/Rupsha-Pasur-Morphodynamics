# Rupsha–Pasur Morphodynamics

## Spatially lagged curvature–migration coupling in a tidal river corridor

**Independent research project · Manuscript in preparation**

This project investigates how antecedent channel geometry relates to subsequent lateral migration along the tidal Rupsha–Pasur river corridor in southwest Bangladesh.

Using multi-decadal Landsat-derived channel geometry, the analysis combines signed channel curvature, width-normalized upstream spatial offsets, lateral centerline migration, measurement-uncertainty assessment, and hierarchical Bayesian distributed-lag modeling.

---

## Research question

**At what upstream spatial offset does channel curvature show the clearest association with subsequent lateral migration, and how does that relationship vary along the river corridor?**

The analysis evaluates curvature at six prespecified upstream positions:

`0.0B · 0.5B · 1.0B · 1.5B · 2.0B · 2.5B`

where **B** is the start-state local channel width at the response station.

---

## Study scale

| Component | Value |
|---|---:|
| Analysis period | 1988–2025 |
| Analyzed river axis | ~121.6 km |
| Inferential observations | 25,923 |
| Unique stations | 1,014 |
| Spatial blocks | 12 |
| Temporal periods | 34 |
| Primary curvature scale | W15 signed, width-normalized curvature |

---

## Analytical workflow

The project integrates:

- topology-aware Landsat channel extraction;
- fixed-axis satellite-observed outer water–land boundary-proxy and centerline geometry;
- channel-width estimation;
- signed channel curvature;
- width-normalized upstream spatial lags;
- signed lateral centerline migration;
- empirical measurement-uncertainty analysis;
- spatial and temporal hierarchical effects; and
- Bayesian Student-t distributed-lag inference.

The lag framework is **spatial rather than temporal**. For a response location at position `s`, curvature at lag `L` is evaluated upstream at:

`target position = s − L × start-state local channel width`

More methodological detail is provided in [`docs/methodology.md`](docs/methodology.md).

---

## Main finding

The clearest corridor-wide association occurs at approximately **2.0 local channel widths upstream**.

For a +1 SD increase in signed curvature at 2.0B, the posterior mean effect on signed centerline migration is:

**-0.085 m yr⁻¹**

with a 95% credible interval of:

**-0.180 to -0.019 m yr⁻¹**

and:

**P(outward-aligned effect) = 0.993**

Under the downstream-referenced coordinate convention used in this study, a negative curvature coefficient represents an **outward-aligned migration tendency**.

The effect is small in corridor-wide magnitude, but the directional tendency is spatially widespread: **10 of 12 spatial blocks** have negative posterior means at 2.0B.

Individual reach-level estimates remain more uncertain than the corridor-wide mean.

---

## Main result figure

![Global and spatially varying curvature–migration coupling](figures/main_curvature_migration_results.png)

The figure summarizes the corridor-wide distributed-lag posterior, block-specific lag responses, and spatial locations of the modeled blocks.

---

## Spatial consistency of the 2.0B signal

![Spatial consistency of the 2.0B effect](figures/twoB_spatial_consistency.png)

Although no individual block has a 95% credible interval entirely below zero at 2.0B, the posterior mean is negative in **10/12 blocks**.

The corridor-wide result is therefore interpreted as a **spatially widespread outward-aligned tendency with substantial local uncertainty**, rather than an effect produced by only one or two reaches.

---

## Reach-scale heterogeneity

Across the complete 0–2.5B lag domain, **4 block-lag effects** have 95% credible intervals excluding zero.

These include both outward- and inward-aligned responses, indicating that the magnitude, direction, and spatial offset of curvature–migration coupling vary along the corridor.

Derived posterior summaries are available in [`results/`](results/).

---

## Statistical model

The final inferential model is a hierarchical Bayesian distributed-lag model with a Student-t likelihood.

It includes:

- corridor-wide lag coefficients;
- block-specific lag deviations;
- channel-width effect;
- continuous along-channel spatial structure;
- station-level effects;
- temporal-period effects; and
- block-period effects.

The robust Student-t likelihood accommodates very heavy-tailed residual behavior.

Two residual NUTS divergences remained among 8,000 retained posterior draws. Dedicated sensitivity analyses showed negligible influence on the reported corridor-wide and block-specific scientific quantities.

See [`docs/results_summary.md`](docs/results_summary.md) for the interpretation record.

---

## Interpretation boundary

This study identifies **conditional associations** between antecedent channel geometry and subsequent lateral migration.

The results should not be interpreted as showing that curvature alone causes migration, nor as evidence of demonstrated out-of-sample predictive performance.

---

## Repository contents

```text
Rupsha-Pasur-Morphodynamics/
├── README.md
├── PROJECT_STATUS.md
├── CITATION.cff
├── environment.yml
├── LICENSE.md
├── LICENSES/
│   ├── MIT.txt
│   └── CC-BY-4.0.md
├── data/
│   ├── README.md
│   └── inferential_model_input.csv.gz
├── docs/
│   ├── methodology.md
│   ├── results_summary.md
│   ├── headline_findings.md
│   └── verified_project_facts.csv
├── figures/
│   ├── main_curvature_migration_results.png
│   └── twoB_spatial_consistency.png
├── notebooks/
│   └── README.md
├── results/
│   ├── global_distributed_lag_results.csv
│   ├── block_specific_lag_results.csv
│   ├── spatial_block_locations.csv
│   └── twoB_evidence_summary.csv
└── src/
    ├── README.md
    ├── bayesian_model.py
    └── results_figures.py
```

Large Landsat scenes, raster intermediates, Monte Carlo realizations, and full posterior files are intentionally excluded from the public repository.

---

## Data and reproducibility

Compact derived scientific outputs are provided in `results/`.

The repository includes the final Bayesian model implementation in `src/bayesian_model.py` and a lightweight figure-reproduction workflow in `src/results_figures.py`. Demonstration notebooks are being prepared separately.

See [`data/README.md`](data/README.md) for the data-availability strategy.

---

## Environment

A Conda environment specification is provided in [`environment.yml`](environment.yml).

Create the environment with:

```bash
conda env create -f environment.yml
conda activate rupsha-pasur-morphodynamics
```

To regenerate the public result figures:

```bash
python src/results_figures.py
```

The figure workflow uses the compact posterior summary tables and does not require re-running the Bayesian sampler.
---

## Project status

**Manuscript in preparation.**

This repository represents an active independent research project. Results may be refined during manuscript preparation and peer review.
---

## Citation

Citation metadata is provided in [`CITATION.cff`](CITATION.cff).

A formal manuscript citation will be added after publication or preprint release.
---

## License

Source code is available under the **MIT License**.

Original figures, documentation, and derived research result tables are available under **CC BY 4.0**.

See [`LICENSE.md`](LICENSE.md) for the scope of each license.