"""
Reproduce the headline Rupsha–Pasur result figures from
compact posterior-summary tables included in the repository.

This script does not require the full posterior or MCMC.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from matplotlib.patches import Rectangle


LAG_ORDER = [
    "0.0B",
    "0.5B",
    "1.0B",
    "1.5B",
    "2.0B",
    "2.5B",
]


def repository_root():
    """Return the repository root from this script location."""

    return Path(__file__).resolve().parents[1]


def load_results(root=None):
    """Load compact public posterior-summary tables."""

    if root is None:
        root = repository_root()

    root = Path(root)

    global_df = pd.read_csv(
        root
        / "results"
        / "global_distributed_lag_results.csv"
    )

    block_df = pd.read_csv(
        root
        / "results"
        / "block_specific_lag_results.csv"
    )

    location_df = pd.read_csv(
        root
        / "results"
        / "spatial_block_locations.csv"
    )

    return global_df, block_df, location_df


def _find_column(frame, candidates):
    """Return the first matching column name, else None."""

    lookup = {
        str(col).lower(): col
        for col in frame.columns
    }

    for candidate in candidates:

        key = candidate.lower()

        if key in lookup:
            return lookup[key]

    return None


def _block_label_column(frame):

    col = _find_column(
        frame,
        [
            "spatial_block_label",
            "block_label",
            "block",
        ],
    )

    if col is None:
        raise ValueError(
            "Could not identify spatial block label field."
        )

    return col


def _longitude_latitude_columns(frame):
    """Detect public longitude/latitude fields if present."""

    lon = _find_column(
        frame,
        [
            "longitude",
            "lon",
            "midpoint_lon",
            "axis_mid_lon",
            "block_mid_lon",
            "mid_lon",
        ],
    )

    lat = _find_column(
        frame,
        [
            "latitude",
            "lat",
            "midpoint_lat",
            "axis_mid_lat",
            "block_mid_lat",
            "mid_lat",
        ],
    )

    return lon, lat


def make_main_results_figure(
    global_df,
    block_df,
    location_df,
    output_file,
):
    """Create a compact three-panel main result figure."""

    output_file = Path(output_file)

    global_df = global_df.copy()
    block_df = block_df.copy()
    location_df = location_df.copy()

    global_df['lag'] = pd.Categorical(
        global_df['lag'].astype(str),
        categories=LAG_ORDER,
        ordered=True,
    )

    block_df['lag'] = pd.Categorical(
        block_df['lag'].astype(str),
        categories=LAG_ORDER,
        ordered=True,
    )

    global_df = global_df.sort_values(
        'lag'
    ).reset_index(drop=True)

    block_label = _block_label_column(
        block_df
    )

    # ----------------------------------------
    # Figure layout
    # ----------------------------------------

    fig = plt.figure(
        figsize=(14, 9)
    )

    gs = fig.add_gridspec(
        2,
        2,
        width_ratios=[1.25, 1.0],
        height_ratios=[1.0, 1.15],
        hspace=0.30,
        wspace=0.22,
    )

    ax_a = fig.add_subplot(
        gs[0, 0]
    )

    ax_b = fig.add_subplot(
        gs[1, 0]
    )

    ax_c = fig.add_subplot(
        gs[:, 1]
    )

    # ----------------------------------------
    # Panel A — global lag response
    # ----------------------------------------

    x = np.arange(
        len(LAG_ORDER),
        dtype=float,
    )

    mean = global_df[
        'mean_migration_m_per_yr_per_1sd_kappaB'
    ].to_numpy(dtype=float)

    low = global_df[
        'q025_migration_m_per_yr_per_1sd_kappaB'
    ].to_numpy(dtype=float)

    high = global_df[
        'q975_migration_m_per_yr_per_1sd_kappaB'
    ].to_numpy(dtype=float)

    yerr = np.vstack(
        [
            mean - low,
            high - mean,
        ]
    )

    ax_a.axhline(
        0.0,
        linestyle='--',
        linewidth=1.0,
    )

    ax_a.errorbar(
        x,
        mean,
        yerr=yerr,
        fmt='o-',
        capsize=4,
        linewidth=1.5,
    )

    ax_a.set_xticks(
        x
    )

    ax_a.set_xticklabels(
        LAG_ORDER
    )

    ax_a.set_xlabel(
        'Upstream curvature offset (B)'
    )

    ax_a.set_ylabel(
        'Effect on migration\n'
        '(m yr$^{-1}$ per +1 SD curvature)'
    )

    ax_a.set_title(
        'A. Corridor-wide distributed-lag response',
        loc='left',
        fontweight='bold',
    )

    # Mark lags with 95% intervals excluding zero.

    for i in range(len(global_df)):

        if (
            low[i] > 0
            or high[i] < 0
        ):

            ax_a.scatter(
                x[i],
                mean[i],
                s=90,
                facecolors='none',
                edgecolors='black',
                linewidths=1.5,
                zorder=5,
            )

    # ----------------------------------------
    # Panel B — block × lag posterior means
    # ----------------------------------------

    if 'axis_mid_km' not in block_df.columns:
        raise ValueError(
            "block_specific_lag_results.csv must contain "
            "axis_mid_km."
        )

    block_order = (
        block_df[
            [
                block_label,
                'axis_mid_km',
            ]
        ]
        .drop_duplicates()
        .sort_values('axis_mid_km')
        [block_label]
        .astype(str)
        .tolist()
    )

    heat = block_df.pivot(
        index=block_label,
        columns='lag',
        values='mean_migration_m_per_yr_per_1sd_kappaB',
    ).loc[
        block_order,
        LAG_ORDER,
    ]

    heat_values = heat.to_numpy(
        dtype=float
    )

    max_abs = float(
        np.nanmax(
            np.abs(
                heat_values
            )
        )
    )

    norm = TwoSlopeNorm(
        vmin=-max_abs,
        vcenter=0.0,
        vmax=max_abs,
    )

    image = ax_b.imshow(
        heat_values,
        aspect='auto',
        cmap='coolwarm_r',
        norm=norm,
    )

    ax_b.set_xticks(
        np.arange(len(LAG_ORDER))
    )

    ax_b.set_xticklabels(
        LAG_ORDER
    )

    ax_b.set_yticks(
        np.arange(len(block_order))
    )

    ax_b.set_yticklabels(
        block_order
    )

    ax_b.set_xlabel(
        'Upstream curvature offset (B)'
    )

    ax_b.set_ylabel(
        'Spatial block'
    )

    ax_b.set_title(
        'B. Block-specific distributed-lag response',
        loc='left',
        fontweight='bold',
    )

    # Outline cells whose 95% interval excludes zero.

    if 'interval_status_95' in block_df.columns:

        status = block_df.pivot(
            index=block_label,
            columns='lag',
            values='interval_status_95',
        ).loc[
            block_order,
            LAG_ORDER,
        ]

        for row_i, label in enumerate(
            block_order
        ):

            for col_i, lag in enumerate(
                LAG_ORDER
            ):

                value = str(
                    status.loc[
                        label,
                        lag,
                    ]
                )

                if value != 'OVERLAPS_ZERO':

                    rectangle = Rectangle(
                        (
                            col_i - 0.5,
                            row_i - 0.5,
                        ),
                        1,
                        1,
                        fill=False,
                        edgecolor='black',
                        linewidth=1.8,
                    )

                    ax_b.add_patch(
                        rectangle
                    )

    colorbar = fig.colorbar(
        image,
        ax=ax_b,
        fraction=0.046,
        pad=0.03,
    )

    colorbar.set_label(
        'Effect (m yr$^{-1}$ per +1 SD curvature)'
    )

    # ----------------------------------------
    # Panel C — spatial block positions
    # ----------------------------------------

    loc_block = _block_label_column(
        location_df
    )

    lon_col, lat_col = (
        _longitude_latitude_columns(
            location_df
        )
    )

    if (
        lon_col is not None
        and lat_col is not None
    ):

        loc = (
            location_df
            .drop_duplicates(
                subset=[loc_block]
            )
            .copy()
        )

        if 'axis_mid_km' in loc.columns:
            loc = loc.sort_values(
                'axis_mid_km'
            )

        ax_c.plot(
            loc[lon_col],
            loc[lat_col],
            linewidth=1.5,
        )

        ax_c.scatter(
            loc[lon_col],
            loc[lat_col],
            s=42,
        )

        for _, row in loc.iterrows():

            ax_c.annotate(
                str(row[loc_block]),
                (
                    row[lon_col],
                    row[lat_col],
                ),
                xytext=(4, 4),
                textcoords='offset points',
                fontsize=8,
            )

        ax_c.set_xlabel(
            'Longitude'
        )

        ax_c.set_ylabel(
            'Latitude'
        )

    else:

        # Fallback if geographic coordinates are absent:
        # show block positions along the analysis axis.

        if 'axis_mid_km' not in location_df.columns:
            raise ValueError(
                "Spatial locations require either lon/lat "
                "or axis_mid_km."
            )

        loc = (
            location_df
            .drop_duplicates(
                subset=[loc_block]
            )
            .sort_values('axis_mid_km')
        )

        zeros = np.zeros(
            len(loc)
        )

        ax_c.plot(
            loc['axis_mid_km'],
            zeros,
            linewidth=1.5,
        )

        ax_c.scatter(
            loc['axis_mid_km'],
            zeros,
            s=42,
        )

        for _, row in loc.iterrows():

            ax_c.annotate(
                str(row[loc_block]),
                (
                    row['axis_mid_km'],
                    0,
                ),
                xytext=(0, 7),
                textcoords='offset points',
                ha='center',
                fontsize=8,
            )

        ax_c.set_xlabel(
            'Distance along analysis axis (km)'
        )

        ax_c.set_yticks([])

    ax_c.set_title(
        'C. Spatial blocks',
        loc='left',
        fontweight='bold',
    )

    fig.suptitle(
        'Curvature–migration coupling in the '
        'Rupsha–Pasur corridor',
        fontweight='bold',
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fig.savefig(
        output_file,
        dpi=300,
        bbox_inches='tight',
    )

    plt.close(fig)


def make_twoB_consistency_figure(
    global_df,
    block_df,
    output_file,
):
    """Plot spatial consistency of the 2.0B effect."""

    output_file = Path(output_file)

    global_2b = global_df.loc[
        global_df['lag'].astype(str)
        == '2.0B'
    ]

    if len(global_2b) != 1:
        raise ValueError(
            "Expected one global 2.0B row."
        )

    global_2b = global_2b.iloc[0]

    block_2b = block_df.loc[
        block_df['lag'].astype(str)
        == '2.0B'
    ].copy()

    block_2b = block_2b.sort_values(
        'axis_mid_km'
    ).reset_index(drop=True)

    block_label = _block_label_column(
        block_2b
    )

    x = block_2b[
        'axis_mid_km'
    ].to_numpy(dtype=float)

    mean = block_2b[
        'mean_migration_m_per_yr_per_1sd_kappaB'
    ].to_numpy(dtype=float)

    low = block_2b[
        'q025_migration_m_per_yr_per_1sd_kappaB'
    ].to_numpy(dtype=float)

    high = block_2b[
        'q975_migration_m_per_yr_per_1sd_kappaB'
    ].to_numpy(dtype=float)

    probability = block_2b[
        'prob_lt_zero'
    ].to_numpy(dtype=float)

    global_mean = float(
        global_2b[
            'mean_migration_m_per_yr_per_1sd_kappaB'
        ]
    )

    global_low = float(
        global_2b[
            'q025_migration_m_per_yr_per_1sd_kappaB'
        ]
    )

    global_high = float(
        global_2b[
            'q975_migration_m_per_yr_per_1sd_kappaB'
        ]
    )

    fig, axes = plt.subplots(
        2,
        1,
        figsize=(11, 8),
        sharex=True,
        gridspec_kw={
            'height_ratios': [1.3, 1.0],
            'hspace': 0.10,
        },
    )

    ax_a, ax_b = axes

    ax_a.axhline(
        0.0,
        linestyle='--',
        linewidth=1.0,
    )

    ax_a.axhspan(
        global_low,
        global_high,
        alpha=0.15,
    )

    ax_a.axhline(
        global_mean,
        linewidth=1.8,
    )

    ax_a.errorbar(
        x,
        mean,
        yerr=np.vstack(
            [
                mean - low,
                high - mean,
            ]
        ),
        fmt='o',
        capsize=4,
        linewidth=1.2,
    )

    for xi, yi, label in zip(
        x,
        mean,
        block_2b[block_label].astype(str),
    ):

        ax_a.annotate(
            label,
            (xi, yi),
            xytext=(0, 7),
            textcoords='offset points',
            ha='center',
            fontsize=8,
        )

    ax_a.set_ylabel(
        '2.0B effect\n'
        '(m yr$^{-1}$ per +1 SD curvature)'
    )

    ax_a.set_title(
        'A. Block-specific 2.0B effects',
        loc='left',
        fontweight='bold',
    )

    ax_b.axhline(
        0.50,
        linestyle='--',
        linewidth=1.0,
    )

    ax_b.axhline(
        0.90,
        linestyle=':',
        linewidth=1.0,
    )

    ax_b.axhline(
        0.95,
        linestyle='-.',
        linewidth=1.0,
    )

    ax_b.plot(
        x,
        probability,
        marker='o',
        linewidth=1.5,
    )

    ax_b.set_ylim(
        0.0,
        1.02,
    )

    ax_b.set_ylabel(
        'P(outward-aligned effect)'
    )

    ax_b.set_xlabel(
        'Distance along analysis axis (km)'
    )

    ax_b.set_title(
        'B. Posterior support for outward alignment',
        loc='left',
        fontweight='bold',
    )

    fig.suptitle(
        'Spatial consistency of the 2.0B '
        'curvature–migration association',
        fontweight='bold',
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fig.savefig(
        output_file,
        dpi=300,
        bbox_inches='tight',
    )

    plt.close(fig)


def main():

    root = repository_root()

    global_df, block_df, location_df = (
        load_results(root)
    )

    main_output = (
        root
        / 'figures'
        / 'reproduced_main_results.png'
    )

    twoB_output = (
        root
        / 'figures'
        / 'reproduced_twoB_spatial_consistency.png'
    )

    make_main_results_figure(
        global_df,
        block_df,
        location_df,
        main_output,
    )

    make_twoB_consistency_figure(
        global_df,
        block_df,
        twoB_output,
    )

    print(
        'Saved:',
        main_output,
    )

    print(
        'Saved:',
        twoB_output,
    )


if __name__ == '__main__':
    main()