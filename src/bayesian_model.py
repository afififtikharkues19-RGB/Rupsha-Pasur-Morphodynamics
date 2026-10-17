"""
Hierarchical Bayesian distributed-lag model for the
Rupsha–Pasur morphodynamics project.

The model evaluates signed, width-normalized channel
curvature at six upstream spatial offsets as predictors of
subsequent signed centerline migration.

The lag dimension is spatial, not temporal.

This module contains the final scientific parameterization
used by the project. Sampling is never started on import.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import pymc as pm
import pytensor.tensor as pt


LAG_LABELS = [
    "0.0B",
    "0.5B",
    "1.0B",
    "1.5B",
    "2.0B",
    "2.5B",
]


LAG_STEP_LABELS = [
    "0.0_to_0.5B",
    "0.5_to_1.0B",
    "1.0_to_1.5B",
    "1.5_to_2.0B",
    "2.0_to_2.5B",
]


LAG_COLUMNS = [
    "kappaB_z_L0p0B",
    "kappaB_z_L0p5B",
    "kappaB_z_L1p0B",
    "kappaB_z_L1p5B",
    "kappaB_z_L2p0B",
    "kappaB_z_L2p5B",
]


AXIS_COLUMNS = [
    f"axis_spline_z_{j:02d}"
    for j in range(1, 9)
]


def load_model_input(path):
    """Load and validate the public inferential design."""

    path = Path(path)

    design = pd.read_csv(
        path,
        low_memory=False,
    )

    required = [
        "M_z",
        "log_width_z",
        "station_re_index",
        "period_index",
        "spatial_block_index",
        "block_period_re_index",
    ] + LAG_COLUMNS + AXIS_COLUMNS

    missing = [
        col
        for col in required
        if col not in design.columns
    ]

    if missing:
        raise ValueError(
            f"Missing model fields: {missing}"
        )

    return design


def prepare_arrays(design):
    """Convert the public design table into model arrays."""

    y = design["M_z"].to_numpy(dtype=np.float64)

    width = design["log_width_z"].to_numpy(
        dtype=np.float64
    )

    lag = design[LAG_COLUMNS].to_numpy(
        dtype=np.float64
    )

    axis = design[AXIS_COLUMNS].to_numpy(
        dtype=np.float64
    )

    station = design["station_re_index"].to_numpy(
        dtype=np.int64
    )

    period = design["period_index"].to_numpy(
        dtype=np.int64
    )

    block = design["spatial_block_index"].to_numpy(
        dtype=np.int64
    )

    block_period = design["block_period_re_index"].to_numpy(
        dtype=np.int64
    )

    for array in [
        y,
        width,
        lag,
        axis,
    ]:

        if not np.isfinite(array).all():
            raise ValueError(
                "Non-finite model input detected."
            )

    return {
        "y": y,
        "width": width,
        "lag": lag,
        "axis": axis,
        "station": station,
        "period": period,
        "block": block,
        "block_period": block_period,
    }


def build_model(design):
    """Build the final hierarchical Student-t model."""

    a = prepare_arrays(design)

    n = len(design)
    n_station = int(a["station"].max()) + 1
    n_period = int(a["period"].max()) + 1
    n_block = int(a["block"].max()) + 1
    n_block_period = int(a["block_period"].max()) + 1

    coords = {
        "obs": np.arange(n),
        "lag": LAG_LABELS,
        "lag_step": LAG_STEP_LABELS,
        "axis_basis": np.arange(8),
        "station": np.arange(n_station),
        "period": np.arange(n_period),
        "block": np.arange(n_block),
        "block_period": np.arange(n_block_period),
    }

    with pm.Model(coords=coords) as model:

        width_data = pm.Data(
            "width_data",
            a["width"],
            dims="obs",
        )

        lag_data = pm.Data(
            "lag_data",
            a["lag"],
            dims=("obs", "lag"),
        )

        axis_data = pm.Data(
            "axis_data",
            a["axis"],
            dims=("obs", "axis_basis"),
        )

        station_data = pm.Data(
            "station_index",
            a["station"],
            dims="obs",
        )

        period_data = pm.Data(
            "period_index",
            a["period"],
            dims="obs",
        )

        block_data = pm.Data(
            "block_index",
            a["block"],
            dims="obs",
        )

        block_period_data = pm.Data(
            "block_period_index",
            a["block_period"],
            dims="obs",
        )

        # Global intercept and width effect.

        alpha = pm.Normal(
            "alpha",
            mu=0.0,
            sigma=0.25,
        )

        beta_width = pm.Normal(
            "beta_width",
            mu=0.0,
            sigma=0.25,
        )

        # Corridor-wide distributed-lag curve.

        beta_lag_0 = pm.Normal(
            "beta_lag_0",
            mu=0.0,
            sigma=0.25,
        )

        tau_lag_increment = pm.HalfNormal(
            "tau_lag_increment",
            sigma=0.15,
        )

        # Non-centered implementation of the locked
        # first-order random-walk prior.

        lag_increment_raw = pm.Normal(
            "lag_increment_raw",
            mu=0.0,
            sigma=1.0,
            dims="lag_step",
        )

        lag_increment = pm.Deterministic(
            "lag_increment",
            tau_lag_increment
            * lag_increment_raw,
            dims="lag_step",
        )

        beta_lag_rest = (
            beta_lag_0
            + pt.cumsum(lag_increment)
        )

        beta_lag = pm.Deterministic(
            "beta_lag",
            pt.concatenate(
                [
                    beta_lag_0[None],
                    beta_lag_rest,
                ],
                axis=0,
            ),
            dims="lag",
        )

        # Block-specific deviations, constrained to have
        # mean zero across blocks at each lag.

        tau_block_lag = pm.HalfNormal(
            "tau_block_lag",
            sigma=0.15,
        )

        block_lag_raw = pm.Normal(
            "block_lag_raw",
            mu=0.0,
            sigma=1.0,
            dims=("block", "lag"),
        )

        block_lag_centered_raw = (
            block_lag_raw
            - pt.mean(
                block_lag_raw,
                axis=0,
                keepdims=True,
            )
        )

        block_lag = pm.Deterministic(
            "block_lag",
            tau_block_lag
            * block_lag_centered_raw,
            dims=("block", "lag"),
        )

        # Continuous along-axis baseline.

        sigma_axis = pm.HalfNormal(
            "sigma_axis",
            sigma=0.30,
        )

        axis_raw = pm.Normal(
            "axis_raw",
            mu=0.0,
            sigma=1.0,
            dims="axis_basis",
        )

        axis_coef = pm.Deterministic(
            "axis_coef",
            sigma_axis * axis_raw,
            dims="axis_basis",
        )

        # Station random intercept.

        sigma_station = pm.HalfNormal(
            "sigma_station",
            sigma=0.50,
        )

        station_raw = pm.Normal(
            "station_raw",
            mu=0.0,
            sigma=1.0,
            dims="station",
        )

        station_effect = pm.Deterministic(
            "station_effect",
            sigma_station * station_raw,
            dims="station",
        )

        # Period random intercept.

        sigma_period = pm.HalfNormal(
            "sigma_period",
            sigma=0.30,
        )

        period_raw = pm.Normal(
            "period_raw",
            mu=0.0,
            sigma=1.0,
            dims="period",
        )

        period_effect = pm.Deterministic(
            "period_effect",
            sigma_period * period_raw,
            dims="period",
        )

        # Block-period random intercept.

        sigma_block_period = pm.HalfNormal(
            "sigma_block_period",
            sigma=0.30,
        )

        block_period_raw = pm.Normal(
            "block_period_raw",
            mu=0.0,
            sigma=1.0,
            dims="block_period",
        )

        block_period_effect = pm.Deterministic(
            "block_period_effect",
            sigma_block_period
            * block_period_raw,
            dims="block_period",
        )

        # Heavy-tailed residual likelihood.

        sigma = pm.HalfNormal(
            "sigma",
            sigma=1.0,
        )

        nu_minus_2 = pm.Exponential(
            "nu_minus_2",
            lam=0.1,
        )

        nu = pm.Deterministic(
            "nu",
            2.0 + nu_minus_2,
        )

        global_lag_effect = pt.sum(
            lag_data
            * beta_lag[None, :],
            axis=1,
        )

        local_lag_effect = pt.sum(
            lag_data
            * block_lag[block_data],
            axis=1,
        )

        spatial_baseline = pt.sum(
            axis_data
            * axis_coef[None, :],
            axis=1,
        )

        mu = (
            alpha
            + beta_width * width_data
            + spatial_baseline
            + station_effect[station_data]
            + period_effect[period_data]
            + block_period_effect[block_period_data]
            + global_lag_effect
            + local_lag_effect
        )

        pm.StudentT(
            "y_obs",
            nu=nu,
            mu=mu,
            sigma=sigma,
            observed=a["y"],
            dims="obs",
        )

    return model


def sample_model(
    model,
    draws=2000,
    tune=1500,
    chains=4,
    cores=1,
    target_accept=0.995,
    random_seed=20261017,
):
    """Sample using the final production sampler settings."""

    with model:
        return pm.sample(
            draws=draws,
            tune=tune,
            chains=chains,
            cores=cores,
            target_accept=target_accept,
            random_seed=random_seed,
            return_inferencedata=True,
        )


if __name__ == '__main__':

    repository_root = (
        Path(__file__).resolve().parents[1]
    )

    input_file = (
        repository_root
        / "data"
        / "inferential_model_input.csv.gz"
    )

    data = load_model_input(input_file)
    model = build_model(data)

    print(model)
    print()
    print(
        "Model constructed successfully. "
        "Sampling was NOT started."
    )