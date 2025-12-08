# Status Report

## Tianqi's Portion: EnviroAtlas BenMAP Dataset and Data Pipeline Notes

So far, I have downloaded the EnviroAtlas New York City BenMAP results dataset from [Data.gov](https://catalog.data.gov/dataset/enviroatlas-new-york-city-ny-benmap-results-by-block-group3), verified its integrity with SHA256 checksums, inspected the data structure, and built a reproducible data pipeline including SQL schema design, import scripts, and basic cleaning automation. Below are detailed findings about the dataset structure, data quality issues identified, and the technical infrastructure created for data integration.

### General Findings

* **Number of rows:** 6,379 (including header; 6,378 block groups)
* **Number of columns:** 151 health impact estimate columns plus the `bgrp` identifier
* **Primary key:** `bgrp` (census block group FIPS code, 12-digit concatenation of state/county/tract/block group)
* **Data format:** All health impact columns are numeric; many contain zeros (indicating no estimated impact for that block group)
* **Negative values:** Present in multiple PM2.5-related columns (documented as "resuspension" effects in the source metadata)
* **Geographic coverage:** Census block groups across all five NYC boroughs (Bronx, Brooklyn, Manhattan, Queens, Staten Island)

### Data Verification and Provenance

To ensure data integrity and reproducibility, I computed SHA256 checksums for both raw CSV files and recorded them in `data/raw/checksums.txt`:

* **NYNY_BenMAP.csv:** `1358504C48CAA53BCD47747E6A3461325EEEF7FD5E91D916B070F9DE171D0117`
* **Air_Quality.csv:** `F07607F1242BA6FE4D0ADCBF2A5F891C3970720D4DFF6A8610744E0508F1D5EA`

These checksums allow verification of file integrity and serve as provenance documentation for the raw data sources.

### Column Structure and Health Impact Indicators

The BenMAP dataset contains 151 columns organized by pollutant type (NO2, O3, PM2.5, SO2) and health outcome. Each pollutant-outcome combination typically has three variants:

* **`_I_Min`**: Minimum incidence estimate
* **`_I`**: Central incidence estimate  
* **`_I_Max`**: Maximum incidence estimate
* **`_V_Min`, `_V`, `_V_Max`**: Corresponding value estimates (likely monetary or disability-adjusted life years)

#### Pollutants and Health Outcomes Covered

| Pollutant | Health Outcomes Measured |
|:----------|:-------------------------|
| **NO2** | Hospital Admissions, Emergency Room Visits, Asthma Exacerbation, Acute Respiratory Symptoms |
| **O3** | Acute Respiratory Symptoms, Hospital Admissions, Mortality, School Loss Days, Emergency Room Visits |
| **PM2.5** | Acute Bronchitis, Acute Myocardial Infarction, Acute Respiratory Symptoms, Asthma Exacerbation, Chronic Bronchitis, Emergency Room Visits, Hospital Admissions (Cardiovascular), Hospital Admissions (Respiratory), Lower Respiratory Symptoms, Mortality, Upper Respiratory Symptoms, Work Loss Days |
| **SO2** | Acute Respiratory Symptoms, Asthma Exacerbation, Emergency Room Visits, Hospital Admissions |

### Data Quality Issues Identified

#### 1. Negative Values in PM2.5 Columns

Multiple PM2.5-related columns contain negative values. According to the source metadata, these represent "resuspension of particles" and are scientifically valid but require careful handling in analysis. Example columns with negative values:

* `PM25_Hospital_Admissions__Cardiovascular_I`
* `PM25_Hospital_Admissions__Respiratory_I`
* `PM25_Emergency_Room_Visits_I`
* `PM25_Mortality_I`

**Solution implemented:** The cleaning script (`scripts/clean_data.py`) adds a `pm25_negative_flag` column to count how many PM2.5 metrics are negative for each block group, enabling sensitivity analysis without removing potentially valid data.

#### 2. High Proportion of Zero Values

Many block groups show zero impacts across multiple health indicators, likely due to:
* Low population density in those areas
* Minimal pollution concentration changes modeled for those locations
* Model limitations at fine geographic scales

**No action required:** Zero values are scientifically valid and should be preserved. Downstream analysis will need to account for this sparsity.

#### 3. Geographic Granularity Mismatch

The BenMAP dataset uses census block groups (`bgrp`), while Kenneth's Air Quality dataset uses Community District-level identifiers (`Geo Join ID`). Block groups are finer geographic units than Community Districts.

**Solution planned:** Implement spatial aggregation to roll up block group health estimates to the Community District level, or create a crosswalk mapping table. This will be addressed in the next phase using either:
* `geopandas` spatial joins with NYC shapefile boundaries
* A published census block group → Community District mapping table

### SQL Schema Design

I created a minimal SQLite schema in `sql/schema.sql` with two main tables:

#### `air_quality` table
```sql
CREATE TABLE air_quality (
  unique_id INTEGER,
  indicator_id INTEGER,
  name TEXT,
  measure TEXT,
  measure_info TEXT,
  geo_type_name TEXT,
  geo_join_id TEXT,
  geo_place_name TEXT,
  time_period TEXT,
  start_date TEXT,
  data_value REAL,
  message TEXT
);
```

#### `benmap` table
The schema file provides a minimal structure (primary key `bgrp` only), as the full 151-column structure is automatically created by the import script using `pandas.to_sql()`, which dynamically infers column types from the CSV.

**Rationale:** Given the large number of columns in BenMAP, dynamic schema creation reduces maintenance burden and ensures all columns are captured without manual enumeration errors.

### Data Import Pipeline

Created `scripts/load_data.py` to automate CSV import into SQLite (`data/nyc_air_health.db`):

**Features:**
* Uses `pandas` with chunked reading (200,000 rows per chunk) for memory efficiency on large files
* Falls back to standard `csv` + `sqlite3` if pandas is unavailable
* Handles both datasets in a single script execution
* Creates or overwrites tables to enable reproducible re-imports

**Usage:**
```powershell
python .\scripts\load_data.py
```

**Output:** `data/nyc_air_health.db` (SQLite database with both tables populated)

### Data Cleaning Pipeline

Created `scripts/clean_data.py` to perform initial cleaning steps:

**Operations performed:**
1. **Time normalization for Air Quality data:**
   * Extracts 4-digit year from `Time Period` field (handles formats like "Winter 2014-15", "Annual Average 2017")
   * Falls back to parsing `Start_Date` if year not found in Time Period
   * Adds a standardized `year` column to enable temporal joins and filtering

2. **PM2.5 negative value flagging for BenMAP data:**
   * Counts number of negative values across all PM2.5-related columns for each block group
   * Adds `pm25_negative_flag` column with the count
   * Preserves original negative values for sensitivity analysis

**Output:** Cleaned CSVs in `data/processed/`:
* `air_quality_clean.csv`
* `NYNY_BenMAP_clean.csv`

### Data Inspection and Documentation

Created `scripts/inspect.py` to generate quick data summaries without requiring pandas:

**Output:** `docs/inspect_report.txt` containing:
* Column counts
* First 20 column names
* Sample rows (up to 5)
* Approximate row counts

Additional documentation created:
* `docs/schema_design.md` – Database design rationale and table structures
* `docs/data_quality_notes.md` – Known issues and planned mitigation strategies
* `data/README.md` – Data directory structure and file descriptions

### Next Steps

1. **Execute the full pipeline:**
   * Run `load_data.py` to populate the SQLite database
   * Run `clean_data.py` to generate cleaned CSVs
   * Verify row counts and spot-check cleaned data

2. **Implement geographic aggregation:**
   * Research census block group → Community District crosswalks
   * Implement spatial join or weighted aggregation script
   * Document aggregation methodology

3. **Hand off cleaned data to Kenneth:**
   * Provide cleaned CSVs or database queries
   * Document join keys and temporal alignment strategies
   * Support integration with Air Quality dataset for analysis

4. **Create data dictionary:**
   * Document all 151 BenMAP columns with units and interpretations
   * Clarify negative value meanings for end users
   * Provide example queries for common analysis tasks

## Kenneth's Portion: City of New York Air Quality Dataset Notes

So far, I have downloaded the data as a CSV file from [Data.gov](http://Data.gov) and inspected it using OpenRefine. Below are explanations and tables outlining the data schema and issues I found. The next order of business would be to consolidate this information with the data quality notes, then thoroughly review the EPA dataset to determine the best way to integrate the two sets. Analysis and visualization will follow.

### General Findings

* Number of rows: 18,862  
* Each Unique ID is numeric and, in fact, unique   
* Each Indicator ID is numeric  
* Each Geo Join ID is numeric  
* Each Data Value is numeric  
* The Time Period column is vague, but Tianqi provided a solution  
* Every cell in the Message column is blank, so it can be removed

### Indicator IDs and Their Meanings

This table records the Names, Measures, and units (Measure Info column) represented by each Indicator ID. The indicator IDs listed below contain issues that are highlighted in bold. 

* 646, 647: The entry “Âµg/m3” arises from an encoding error with the mu character, and can be changed to “mcg/m3”  
* 652: The “per 100,000” measure does not specify whether it refers to adults or children, as the other “per 100,000” measures do, so it may need to be assumed that both populations are represented  
* 653, 659: The final two show a grammatical mistake that can be corrected to “department”

| Indicator ID | Name | Measure | Measure Info |
| :---- | :---- | :---- | :---- |
| 365 | Fine particles (PM 2.5) | Mean | mcg/m3 |
| 375 | Nitrogen dioxide (NO2) | Mean | ppb |
| 386 | Ozone (O3) | Mean | ppb |
| 639 | Deaths due to PM2.5 | Estimated annual rate (age 30+) | per 100,000 adults |
| 640 | Boiler Emissions- Total SO2 Emissions | Number per km2 | number |
| 641 | Boiler Emissions- Total PM2.5 Emissions | Number per km2 | number |
| 642 | Boiler Emissions- Total NOx Emissions | Number per km2 | number |
| 643 | Annual vehicle miles traveled | Million miles | per square mile |
| 644 | Annual vehicle miles traveled (cars) | Million miles | per square mile |
| 645 | Annual vehicle miles traveled (trucks) | Million miles | per square mile |
| 646 | Outdoor Air Toxics \- Benzene | Annual average concentration | **Âµg/m3** |
| 647 | Outdoor Air Toxics \- Formaldehyde | Annual average concentration | **Âµg/m3** |
| 648 | Asthma emergency department visits due to PM2.5 | Estimated annual rate (under age 18\) | per 100,000 children |
| 650 | Respiratory hospitalizations due to PM2.5 (age 20+) | Estimated annual rate | per 100,000 adults |
| 651 | Cardiovascular hospitalizations due to PM2.5 (age 40+) | Estimated annual rate | per 100,000 adults |
| 652 | Cardiac and respiratory deaths due to Ozone | Estimated annual rate | **per 100,000** |
| 653 | **Asthma emergency departments visits due to Ozone** | Estimated annual rate (under age 18\) | per 100,000 children |
| 655 | Asthma hospitalizations due to Ozone | Estimated annual rate (under age 18\) | per 100,000 children |
| 657 | Asthma emergency department visits due to PM2.5 | Estimated annual rate (age 18+) | per 100,000 adults |
| 659 | **Asthma emergency departments visits due to Ozone** | Estimated annual rate (age 18+) | per 100,000 adults |
| 661 | Asthma hospitalizations due to Ozone | Estimated annual rate (age 18+) | per 100,000 adults |

### Geo Type Names

The Geo Type Name column represents the type of geographic area measured, including the whole of New York City (Citywide), its five boroughs, 59 community districts (CD), and UHF34 and UHF42 districts, which are the two districting methods of the United Hospital Fund of New York. The numbers in the two UHF schemes represent the number of districts; specifically, there are 34 and 42 districts in each, respectively. 

### Boroughs and Citywide Geo Join IDs

The Geo Join ID codes each Geo Type to a number, but these IDs are not always unique. The table below shows how the ID for “Citywide” and “Bronx” are the same. A possible solution is to change the Citywide Geo Join ID to 0, making it unique to the column. However, the purpose of the Geo Join ID is to map data to other datasets, so further inspection of our EPA set in this regard is required.

| Geo Join ID | Geo Type Name | Geo Place Name |
| :---- | :---- | :---- |
| **1** | Borough | Bronx |
| **1** | Citywide | New York City |
| 2 | Borough | Brooklyn |
| 3 | Borough | Manhattan |
| 4 | Borough | Queens |
| 5 | Borough | Staten Island |

### Limitations of Some Geo Types

The table below shows which Indicators are recorded for each Geo Type. Notice how the only Geo Types that record data for every Indicator are Citywide, the boroughs, and the UHF42 districts.

| Geo Type Name | Indicator IDs with Data |
| :---- | :---- |
| Borough | Each borough records all IDs |
| CD | 365, 375, 386, 643, 644, 645, 646, 647 |
| Citywide | All IDs |
| UHF34 | 365, 375, 386 |
| UHF42 | Each district records all IDs |

### UHF42 Geo Join IDs

Due to these limitations, I have only thoroughly inspected the UHF42 Geo Type for now. Still, at a cursory glance at the other Geo Types, several of the IDs from the two UHF types overlap. This is because UHF district IDs are based on location, so UHF42 district 101 is in the Bronx because the first number “1” corresponds to the Bronx’s Geo Join ID, and the “01” is derived from it being the upper-leftmost of the Bronx districts. The same applies to UHF32. 

The table below links the UHF42 Geo Join IDs to their corresponding place names, highlighting some errors in bold based on the codebook and map shown in UHF42\_index.pdf. The list of GEO Join IDs below explains these errors. I also searched Apple Maps to double-check the Geo Place Names that did not match the codebook to verify the correct name of the locations they meant to reference. Note that I have not yet ensured every district actually encompasses the locations it is named after.

* 103: The “Pk” in “Fordham \- Bronx Pk” should be changed to “Park”  
* 105: “High Bridge \- Morrisania” likely refers to the neighborhood called Highbridge (with no space) in this district. Although a bridge literally called High Bridge exists in the neighborhood, the district is likely named after the neighborhood itself, and should probably be changed to reflect that. However, it would be more appropriate to conform to the UHF code rather than to more accurate semantics  
* 202: “Downtown \- Heights \- Slope” should be “Downtown \- Heights \- Park Slope”  
  * Again, “Downtown Brooklyn \- Crown Heights \- Park Slope” would be a more accurate description of the neighborhoods, but I have yet to see a codebook with district 202 named that way  
* 301: This district also covers Inwood, so it is supposed to be “Washington Heights \- Inwood”  
* 410: Rockaways is a spelling error; it should be “Rockaway”

| Geo Join ID | Geo Place Name |
| :---- | :---- |
| 101  | Kingsbridge \- Riverdale |
| 102 | Northeast Bronx |
| 103 | **Fordham \- Bronx Pk** |
| 104 | Pelham \- Throgs Neck |
| 105 | Crotona \-Tremont |
| 106 | **High Bridge \- Morrisania** |
| 107 | Hunts Point \- Mott Haven |
| 201 | Greenpoint |
| 202 | **Downtown \- Heights \- Slope** |
| 203 | Bedford Stuyvesant \- Crown Heights |
| 204 | East New York |
| 205 | Sunset Park |
| 206 | Borough Park |
| 207 | East Flatbush \- Flatbush |
| 208 | Canarsie \- Flatlands |
| 209 | Bensonhurst \- Bay Ridge |
| 210 | Coney Island \- Sheepshead Bay |
| 211 | Williamsburg \- Bushwick |
| 301 | **Washington Heights** |
| 302 | Central Harlem \- Morningside Heights |
| 303 | East Harlem |
| 304 | Upper West Side |
| 305 | Upper East Side |
| 306 | Chelsea \- Clinton |
| 307 | Gramercy Park \- Murray Hill |
| 308 | Greenwich Village \- SoHo |
| 309 | Union Square \- Lower East Side |
| 310 | Lower Manhattan |
| 401 | Long Island City \- Astoria |
| 402 | West Queens |
| 403 | Flushing \- Clearview |
| 404 | Bayside \- Little Neck |
| 405 | Ridgewood \- Forest Hills |
| 406 | Fresh Meadows |
| 407 | Southwest Queens |
| 408 | Jamaica |
| 409 | Southeast Queens |
| 410 | **Rockaways** |
| 501 | Port Richmond |
| 502 | Stapleton \- St. George |
| 503 | Willowbrook |
| 504 | South Beach \- Tottenville |

