# Data availability

Large source and intermediate geospatial datasets are not stored
directly in this GitHub repository.

## Source imagery

The research workflow uses Landsat imagery for multi-decadal
channel reconstruction.

Raw satellite scenes are excluded from the repository because of
their size and because they can be obtained from the original
data providers.

## Large derived products

The following types of files are also excluded from GitHub:

- annual raster water masks
- topology-support rasters
- large intermediate GeoPackages
- full posterior NetCDF files
- Monte Carlo uncertainty realizations
- temporary QC products

## Public derived results

Compact derived scientific outputs used to reproduce the reported
results are provided in the repository's `results/` directory.

These include:

- global distributed-lag posterior summaries
- block-specific lag summaries
- spatial block locations
- evidence-classification summaries

## Reproducibility

Processing and analysis code will be organized under `src/` and
`notebooks/`.

The repository is intended to document the analytical workflow
without duplicating large remotely available satellite datasets.

## Public inferential model input

`inferential_model_input.csv.gz` contains the minimal standardized design matrix required to construct the published Bayesian model.

It contains:

- standardized signed migration response;
- standardized log channel width;
- six standardized signed curvature-lag predictors;
- eight standardized along-axis spline basis variables;
- station, period, spatial-block, and block-period indices.

Raw satellite imagery, annual raster products, and large uncertainty ensembles are not included.