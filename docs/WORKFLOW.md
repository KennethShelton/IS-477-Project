# Workflow Documentation

This document describes the complete data processing and analysis workflow for the NYC Air Quality and Health project.

## Overview

The workflow consists of four main stages:
1. **Inspection**: Examine raw data structure
2. **Loading**: Import data into SQLite database
3. **Cleaning**: Normalize and flag data quality issues
4. **Analysis**: Integrate datasets and compute correlations

## Automated Workflow

### Run All Script
```bash
python scripts/run_all.py
```

This script executes the entire pipeline sequentially. It will:
- Inspect raw data and generate a report
- Load CSVs into SQLite database
- Clean and normalize data
- Run analysis and generate visualizations

## Individual Script Details

### 1. `scripts/inspection.py`
**Purpose**: Quick data profiling  
**Input**: `data/raw/*.csv`  
**Output**: `docs/inspect_report.txt`

Generates a text report containing:
- Column names and data types
- Row counts
- Sample values
- Basic statistics

### 2. `scripts/load_data.py`
**Purpose**: Import raw data into relational database  
**Input**: `data/raw/air_quality.csv`, `data/raw/NYNY_BenMAP.csv`  
**Output**: `data/nyc_air_health.db` (SQLite database)

Process:
- Creates SQLite database
- Imports CSVs using pandas (with fallback to csv module)
- Preserves all columns and data types

### 3. `scripts/clean_data.py`
**Purpose**: Data normalization and quality flagging  
**Input**: `data/raw/*.csv`  
**Output**: `data/processed/*_clean.csv`

Cleaning operations:
- **Air Quality**: 
  - Extracts year from `Time Period` or `Start_Date`
  - Normalizes date formats
  - Adds `year` column
- **BenMAP**:
  - Flags negative PM2.5 values
  - Adds `pm25_negative_flag` column (count of negative values)

### 4. `scripts/analysis.py`
**Purpose**: Data integration and correlation analysis  
**Input**: `data/processed/*_clean.csv`  
**Output**: 
- `data/processed/merged.csv`
- `docs/correlation.png`

Analysis steps:
1. Filter Air Quality data to borough level
2. Select target pollutants (NO2, O3, PM2.5)
3. Calculate mean pollutant values by borough
4. Map BenMAP block groups to boroughs using FIPS codes
5. Aggregate health symptom incidences by borough
6. Merge datasets on borough and pollutant
7. Calculate Pearson correlation coefficients
8. Generate heatmap visualization

## Jupyter Notebooks

### `scripts/integration.ipynb`
Interactive notebook demonstrating the data integration logic. Contains the same analysis as `analysis.py` but in step-by-step cells for exploration.

### `scripts/workflow.ipynb`
Comprehensive notebook combining all workflow stages. Can be used as an alternative to running individual scripts.

## Data Flow Diagram

```
data/raw/
├── air_quality.csv ────┐
└── NYNY_BenMAP.csv ────┤
                        ↓
                [inspection.py]
                        ↓
                docs/inspect_report.txt
                        
data/raw/               
├── air_quality.csv ────┐
└── NYNY_BenMAP.csv ────┤
                        ↓
                [load_data.py]
                        ↓
                data/nyc_air_health.db
                        
data/raw/               
├── air_quality.csv ────┐
└── NYNY_BenMAP.csv ────┤
                        ↓
                [clean_data.py]
                        ↓
        data/processed/
        ├── air_quality_clean.csv
        └── NYNY_BenMAP_clean.csv
                        ↓
                [analysis.py]
                        ↓
        ┌───────────────┴───────────────┐
        ↓                               ↓
data/processed/merged.csv       docs/correlation.png
```

## Reproducibility Notes

- All scripts are idempotent (safe to run multiple times)
- Raw data files are not modified
- Processed files are overwritten on each run
- Database is recreated if it exists
- Random seeds are not applicable (no stochastic processes)

## Dependencies

See `requirements.txt`:
- pandas >= 1.5.0
- matplotlib >= 3.8.4
- seaborn >= 0.13.2
- numpy >= 1.26.4

SQLite3 is included with Python standard library.
