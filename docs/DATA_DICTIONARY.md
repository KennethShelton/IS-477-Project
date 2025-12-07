# Data Dictionary

## Air Quality Dataset (`air_quality_clean.csv`)

| Column Name | Data Type | Description | Example Values |
|-------------|-----------|-------------|----------------|
| Unique ID | Integer | Unique record identifier | 336867 |
| Indicator ID | Integer | Identifier for the type of measured indicator | 375 |
| Name | Text | Name of the air quality indicator | "Nitrogen dioxide (NO2)", "Ozone (O3)" |
| Measure | Text | Statistical measure used | "Mean", "Annual Average" |
| Measure Info | Text | Units and additional information about the measure | "ppb", "mcg/m3" |
| Geo Type Name | Text | Geographic aggregation level | "Borough", "UHF42", "Citywide" |
| Geo Join ID | Text | Geographic identifier for mapping | "407", "Bronx" |
| Geo Place Name | Text | Human-readable location name | "Bronx", "Upper West Side (CD7)" |
| Time Period | Text | Description of the time range | "Winter 2014-15", "Annual Average 2020" |
| Start_Date | Text | Start date of measurement period | "12/01/2014", "2020-01-01" |
| Data Value | Numeric | Measured value for the indicator | 27.42, 19.43 |
| Message | Text | Notes or flags about the data value | Usually empty |
| year | Text | Extracted year from Time Period or Start_Date | "2014", "2020" |

## BenMAP Health Impact Dataset (`NYNY_BenMAP_clean.csv`)

| Column Name | Data Type | Description | Example Values |
|-------------|-----------|-------------|----------------|
| bgrp | Integer | Census block group FIPS code (12-digit) | 360050001001 |
| NO2_Acute_Respiratory_Symptoms_I | Numeric | Incidence of acute respiratory symptoms due to NO2 | 0.0023, 0.0045 |
| O3_Acute_Respiratory_Symptoms_I | Numeric | Incidence of acute respiratory symptoms due to O3 | 0.0156, 0.0234 |
| PM25_Acute_Respiratory_Symptoms_I | Numeric | Incidence of acute respiratory symptoms due to PM2.5 | 0.0089, -0.0012 |
| NO2_Hospital_Admissions_I | Numeric | Hospital admissions incidence due to NO2 | 0.0001, 0.0003 |
| O3_Hospital_Admissions_I | Numeric | Hospital admissions incidence due to O3 | 0.0002, 0.0005 |
| PM25_Hospital_Admissions_I | Numeric | Hospital admissions incidence due to PM2.5 | 0.0003, -0.0001 |
| pm25_negative_flag | Integer | Count of PM2.5-related columns with negative values | 0, 3, 12 |
| *(many more health outcome columns)* | Numeric | Various health impact estimates | varies |

**Note on Negative Values**: Negative values in PM2.5 health impact columns represent "resuspension" effects where particles are re-emitted into the air, potentially reducing net exposure.

**FIPS Code Ranges by Borough**:
- Bronx: 360050000000 - 360059999999
- Brooklyn: 360470000000 - 360479999999
- Manhattan: 360610000000 - 360619999999
- Queens: 360810000000 - 360819999999
- Staten Island: 360850000000 - 360859999999

## Integrated Dataset (`merged.csv`)

| Column Name | Data Type | Description | Example Values |
|-------------|-----------|-------------|----------------|
| Geo Place Name | Text | Borough name | "Bronx", "Manhattan" |
| Indicator ID | Integer | Air quality indicator ID | 375, 386, 365 |
| Name | Text | Pollutant name | "Nitrogen dioxide (NO2)" |
| Measure Info | Text | Units of measurement | "ppb", "mcg/m3" |
| Mean Measure Value | Numeric | Mean pollutant concentration for the borough | 19.43, 31.17 |
| Symptom Type | Text | Health outcome column identifier | "NO2_Acute_Respiratory_Symptoms_I" |
| Symptom Value | Numeric | Total incidence count for the borough | 3, 594, 428 |

This dataset combines borough-level air quality averages with aggregated health symptom incidences, enabling correlation analysis between pollution levels and health outcomes.
