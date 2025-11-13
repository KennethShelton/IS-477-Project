# Data quality notes (initial)

Based on the dataset documentation and quick inspection, these are the main data quality issues to address:

- Time formats are inconsistent in `air_quality.csv` (`Time Period` like "Winter 2014-15", "Annual Average 2017", and `Start_Date` sometimes uses `MM/DD/YYYY` or `YYYY-MM-DD`). Plan: normalize to a `year` field.

- Geographic units differ: `air_quality.csv` uses `Geo Join ID` (neighborhood / CD / community district), while `NYNY_BenMAP.csv` uses `bgrp` (census block group). Plan: perform spatial aggregation (block groups -> neighborhood) or create a mapping table.

- EnviroAtlas BenMAP contains negative values for some PM2.5 metrics (documented as "resuspension"). Plan: preserve negative values but flag them and run sensitivity analyses.

- Missing or zero values appear common for many block groups; quantify missingness and consider imputation strategies or exclusion thresholds.

- Units: verify units for all pollutant measures (e.g., ppb vs µg/m3) before any direct comparison or modeling.
