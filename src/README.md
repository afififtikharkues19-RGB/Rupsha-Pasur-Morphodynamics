# Source code

## `bayesian_model.py`

Constructs the final hierarchical Bayesian distributed-lag model used for the reported curvature–migration inference.

The model includes:

- corridor-wide distributed-lag coefficients;
- a non-centered first-order random-walk lag prior;
- mean-zero block-specific lag deviations;
- an along-axis spline baseline;
- station random intercepts;
- period random intercepts;
- block-period random intercepts; and
- a Student-t residual likelihood.

Running the model script directly constructs the model but does not automatically begin MCMC.

## `results_figures.py`

Regenerates the headline result figures directly from the compact posterior-summary CSV files in `results/`.

Run from the repository root with:

```bash
python src/results_figures.py
```

This produces:

- `figures/reproduced_main_results.png`
- `figures/reproduced_twoB_spatial_consistency.png`

The figure-reproduction workflow does not require the full posterior or re-running MCMC.