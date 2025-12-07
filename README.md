# IS 477 Course Project: Air Quality and Health in NYC

**Team:** Kenneth Shelton & Tianqi Fu  
**Course:** IS 477, Fall 2025

## Contributors
*   **Kenneth Shelton**: Data analysis, visualization, documentation, reproducibility checks.
*   **Tianqi Fu**: Data collection, verification, storage (SQL), data cleaning, integration pipeline.

## Summary
This project investigates the relationship between air pollution and health outcomes in New York City. The primary research question is: *Which air pollutants are most prevalent in New York City, where are they most prevalent, and how are they correlated with respiratory health conditions?* Air pollution represents one of the most significant environmental health challenges facing urban populations globally, and New York City, as one of the largest metropolitan areas in the United States, provides an ideal case study for examining these relationships.

We utilized two primary datasets for this analysis. The first is the NYC Air Quality dataset from the New York City Department of Health and Mental Hygiene, which provides comprehensive measurements of various air pollutants including Nitrogen Dioxide (NO2), Ozone (O3), and Fine Particulate Matter (PM 2.5) across different geographic areas and time periods within the city. This dataset contains over 18,000 records spanning multiple years and geographic granularities, from citywide measurements to specific neighborhood-level data. The second dataset is the EnviroAtlas BenMAP results from the USDA Forest Service, which provides estimated health impact assessments at the census block group level, including predicted incidences of acute respiratory symptoms, hospital admissions, and emergency room visits attributable to changes in air pollutant concentrations.

By integrating these datasets at the borough level, we analyzed the correlation between key pollutants (Nitrogen Dioxide, Ozone, PM 2.5) and acute respiratory symptoms across New York City's five boroughs: Manhattan, Brooklyn, Queens, the Bronx, and Staten Island. The integration process involved aggregating fine-grained block group data to the borough level using FIPS (Federal Information Processing Standards) codes, calculating mean pollutant concentrations for each borough, and computing Pearson correlation coefficients between pollution levels and health outcomes.

Our findings indicate varying degrees of correlation between pollutant levels and reported health symptoms across different boroughs, highlighting the complex nature of environmental health impacts. The analysis revealed that Ozone showed the strongest positive correlation with respiratory symptoms, while the relationship for PM 2.5 was unexpectedly negative, potentially due to data artifacts or temporal misalignment. These results contribute to the broader understanding of urban environmental health and provide actionable insights for public health policy and intervention strategies in densely populated metropolitan areas.

## Data Profile

### 1. New York City Air Quality
*   **Source**: [NYC Open Data / Data.gov](https://catalog.data.gov/dataset/air-quality)
*   **Publisher**: New York City Department of Health and Mental Hygiene (DOHMH)
*   **Description**: This comprehensive dataset contains measurements and surveillance data on air quality across New York City from 2009 to present. It includes measures of various air pollutants such as Nitrogen Dioxide (NO2), Ozone (O3), Fine Particulate Matter (PM 2.5), Sulfur Dioxide (SO2), as well as related public health indicators including asthma emergency department visits and vehicle miles traveled. The data is collected through a network of monitoring stations and reported at multiple geographic scales including citywide, borough-level, United Hospital Fund (UHF) neighborhoods, and Community Districts.
*   **Format**: CSV (Comma-Separated Values), approximately 2.2 MB
*   **Records**: Over 18,000 observations
*   **Key Columns**: `Unique ID` (record identifier), `Indicator ID` (measure type), `Name` (pollutant or indicator name), `Measure` (statistical aggregation method), `Measure Info` (units such as ppb or mcg/m3), `Geo Type Name` (geographic level), `Geo Place Name` (location name), `Time Period` (temporal description), `Start_Date` (period start date), `Data Value` (measured concentration or count), `Message` (data flags or notes).
*   **Temporal Coverage**: 2009-2023 (varies by indicator)
*   **Spatial Coverage**: New York City (5 boroughs, 42 UHF neighborhoods, 59 Community Districts)
*   **Update Frequency**: Annually
*   **Ethical/Legal Considerations**: This is public domain data provided by the NYC government under the NYC Open Data Terms of Use. The dataset contains no personally identifiable information (PII) and represents aggregated population-level statistics. All measurements are derived from environmental monitoring equipment and do not include individual health records. The data is freely available for research, education, and commercial purposes without restrictions.

### 2. EnviroAtlas New York City (BenMAP)
*   **Source**: [Data.gov](https://catalog.data.gov/dataset/enviroatlas-new-york-city-ny-benmap-results-by-block-group3)
*   **Publisher**: United States Department of Agriculture (USDA) Forest Service, with support from the Davey Tree Expert Company
*   **Description**: This dataset provides modeled estimates of health impacts resulting from changes in air pollutant concentrations across New York City. Using the EPA's Benefits Mapping and Analysis Program (BenMAP), the data estimates the incidence of various health outcomes—including acute respiratory symptoms, hospital admissions, emergency room visits, and mortality—attributable to changes in NO2, O3, PM2.5, and SO2 concentrations. The estimates are provided at the census block group level, offering fine spatial resolution for 6,378 block groups across the NYC metropolitan area.
*   **Format**: CSV (Comma-Separated Values), approximately 8 MB
*   **Records**: 6,378 census block groups
*   **Key Columns**: `bgrp` (12-digit FIPS census block group code), `NO2_Acute_Respiratory_Symptoms_I` (incidence count), `NO2_Hospital_Admissions_I`, `O3_Acute_Respiratory_Symptoms_I`, `O3_Hospital_Admissions_I`, `O3_Mortality_I`, `PM25_Acute_Respiratory_Symptoms_I`, `PM25_Hospital_Admissions_Cardiovascular_I`, `PM25_Hospital_Admissions_Respiratory_I`, `PM25_Emergency_Room_Visits_I`, `PM25_Mortality_I`, `SO2_Hospital_Admissions_I`, `SO2_Emergency_Room_Visits_I`, and many additional health outcome estimates.
*   **Temporal Coverage**: Based on 2010 Census geography and air quality modeling scenarios
*   **Spatial Coverage**: New York City metropolitan area (6,378 block groups)
*   **Methodology**: BenMAP modeling uses concentration-response functions derived from epidemiological studies combined with population data and baseline health statistics to estimate health impacts.
*   **Important Note**: Negative values appear in some PM2.5-related columns. According to the data documentation, these represent "resuspension" effects where particles are re-emitted into the air, potentially reducing net exposure in certain scenarios.
*   **Ethical/Legal Considerations**: As a product of U.S. federal government work, this dataset is in the public domain and not subject to copyright protection. The data represents modeled estimates based on population aggregates and does not contain individual health records. All estimates are provided at the census block group level (typically 600-3,000 people), ensuring privacy protection. The data is freely available for any purpose without restriction.

## Data Quality
We performed a rigorous multi-stage quality assessment following established data curation best practices. Our quality evaluation addressed the dimensions of completeness, consistency, validity, accuracy, and fitness-for-use.

**Completeness Assessment**: We systematically checked for missing values across all key columns in both datasets. In the Air Quality dataset, approximately 3% of records had missing `Data Value` fields, particularly for certain pollutant-time-location combinations. These missing values were documented in our data quality notes and excluded from analysis rather than imputed, as the missingness appeared to be systematic (certain monitoring stations were offline during specific periods). The `Message` field, while mostly empty, occasionally contained important contextual notes that we preserved. In the BenMAP dataset, completeness was high (>99.9%), with only a handful of block groups having null values for specific health outcomes, likely due to zero population in those areas.

**Consistency Issues and Resolution**: The Air Quality dataset presented significant consistency challenges, particularly with temporal data. The `Time Period` field used inconsistent free-text descriptions (e.g., "Annual Average 2020", "Winter 2014-15", "Summer 2019 (June-August)"), making temporal aggregation difficult. Additionally, the `Start_Date` field exhibited mixed date formats—some records used `mm/dd/yyyy` format while others used `yyyy-mm-dd` ISO format. Our cleaning pipeline (`scripts/clean_data.py`) addressed this by extracting a normalized `year` field using regular expressions and date parsing logic, attempting multiple format parsers and falling back gracefully when extraction failed. We documented 47 records where year extraction was ambiguous and required manual review.

**Validity and Range Checks**: The BenMAP dataset contained negative values for several PM2.5-related health impact columns. Initial analysis flagged these as potential data errors; however, consultation with the data documentation revealed that these represent "resuspension" effects where particulate matter is re-emitted into the atmosphere, potentially reducing net exposure. We added a `pm25_negative_flag` column during cleaning to count the number of negative values per record, allowing us to stratify analysis by this characteristic. In total, 892 block groups (14% of the dataset) exhibited at least one negative PM2.5 value. For borough-level aggregation, we included these negative values in the sum, representing the net health impact. Geographic validity was checked by ensuring all FIPS codes fell within the expected ranges for New York City counties (Bronx: 36005, Kings/Brooklyn: 36047, New York/Manhattan: 36061, Queens: 36081, Richmond/Staten Island: 36085).

**Granularity Mismatch and Integration Challenges**: A fundamental challenge was the spatial granularity mismatch between datasets. Air Quality data is available at multiple geographic levels (Citywide, Borough, UHF42 neighborhood, Community District), while BenMAP data is at the census block group level (6,378 units). To enable integration, we aggregated BenMAP data to the borough level using FIPS code range mappings (e.g., block groups 360050000000-360059999999 represent the Bronx). This aggregation was necessary but resulted in loss of spatial detail. We calculated mean pollutant concentrations from the Air Quality data for borough-level records only, filtering out finer geographic scales to maintain consistency. This decision was documented as a limitation in our analysis.

**Duplicate Detection**: We checked for duplicate records in both datasets. The Air Quality dataset's `Unique ID` field was indeed unique (no duplicates found). The BenMAP dataset used `bgrp` as the primary key, and we verified uniqueness (6,378 unique block groups, matching the record count).

**Outlier Analysis**: We examined the distribution of pollutant values and health outcomes for outliers. Several NO2 measurements exceeded 40 ppb, which while high, are plausible for urban areas near major traffic corridors. One PM2.5 value exceeded 20 mcg/m3, consistent with episodic pollution events. We retained these values as they represent real environmental conditions rather than measurement errors.

**Fitness-for-Use Evaluation**: Given our research question focusing on borough-level correlations between pollution and health outcomes, both datasets were deemed fit for purpose after cleaning and integration. However, we noted that temporal misalignment (Air Quality data spans 2009-2023 while BenMAP estimates are based on 2010 scenarios) introduces uncertainty into the correlation analysis, as health impacts modeled for 2010 conditions may not reflect current pollutant levels. This temporal disconnect is a key limitation discussed in our Future Work section.

## Findings
We analyzed the correlation between mean pollutant levels and the total incidence of acute respiratory symptoms in each of New York City's five boroughs. Our analysis integrated borough-level air quality measurements with aggregated health impact estimates, producing a merged dataset of 15 records (5 boroughs × 3 pollutants). Pearson correlation coefficients were calculated between mean pollutant concentrations and symptom incidence counts, yielding the following results:

**Ozone (O3): r = 0.38 (Moderate Positive Correlation)**  
Ozone demonstrated the strongest association with acute respiratory symptoms among the three pollutants examined. This moderate positive correlation indicates that boroughs with higher average ozone concentrations tend to experience higher incidences of acute respiratory symptoms. This finding aligns with the established epidemiological literature on ground-level ozone, which is formed through photochemical reactions involving nitrogen oxides and volatile organic compounds in the presence of sunlight. Ozone is a known respiratory irritant that can cause inflammation of airways, reduce lung function, and trigger asthma attacks. The borough-level variation we observed suggests that areas with higher vehicular traffic and industrial activity, combined with meteorological conditions favorable to ozone formation, experience disproportionate health burdens. Manhattan, despite having the highest population density, showed moderate ozone levels (27.4 ppb mean) with 738 symptom incidences, while Brooklyn exhibited both higher ozone levels (32.0 ppb) and the highest symptom count (1,424 incidences).

**Nitrogen Dioxide (NO2): r = 0.26 (Weak to Moderate Positive Correlation)**  
Nitrogen Dioxide showed a weak to moderate positive correlation with respiratory symptoms. As a primary pollutant emitted directly from combustion processes—particularly vehicle exhaust and power generation—NO2 is a key indicator of traffic-related air pollution. The relatively weaker correlation compared to ozone may reflect several factors: (1) NO2 concentrations are more spatially heterogeneous, with hotspots near major roadways that may not be well-captured by borough-level averaging; (2) NO2 can act as both a direct respiratory irritant and a precursor to ozone formation, complicating its independent effects; (3) temporal variability in traffic patterns may introduce noise into the borough-level aggregation. Manhattan exhibited the highest mean NO2 concentration (25.4 ppb), reflecting its dense traffic and urban canyon effects that trap pollutants, yet had relatively low symptom incidence (8 cases), possibly due to underreporting or differences in population age structure and baseline health status.

**Fine Particles (PM 2.5): r = -0.21 (Weak Negative Correlation)**  
The unexpected weak negative correlation between PM 2.5 concentrations and respiratory symptoms presents a counterintuitive finding that requires careful interpretation. Several factors may contribute to this result: (1) **Resuspension Artifacts**: As documented in the data quality section, the BenMAP dataset contains negative values for PM 2.5 health impacts representing particle resuspension. When aggregated to the borough level, these negative values partially offset positive health impacts, potentially distorting the true relationship; (2) **Temporal Misalignment**: The Air Quality data spans 2009-2023 while BenMAP estimates are based on 2010 modeling scenarios. Changes in PM 2.5 sources and concentrations over this period may have disrupted the correlation; (3) **Non-linear Relationships**: The health effects of PM 2.5 may exhibit threshold effects or non-linear dose-response relationships that are not captured by simple linear correlation; (4) **Confounding Variables**: PM 2.5 composition varies by source (vehicular, industrial, biomass burning, secondary formation), and different PM 2.5 components may have varying toxicity. Borough-level aggregation masks this chemical heterogeneity. Manhattan, with the highest mean PM 2.5 concentration (10.2 mcg/m3), had moderate symptom incidence (494 cases), while the Bronx, with lower PM 2.5 (9.1 mcg/m3), had fewer symptoms (428 cases), consistent with the negative correlation.

**Cross-Borough Patterns**  
Brooklyn consistently showed the highest health impact across all pollutants, with 1,424 O3-related symptoms, 23 NO2-related symptoms, and 915 PM 2.5-related symptoms. This may reflect Brooklyn's large population (approximately 2.7 million residents), diverse land use mixing residential, industrial, and commercial areas, and proximity to major transportation corridors. Staten Island, the least populous borough, consistently showed the lowest symptom counts despite moderate pollutant levels, likely reflecting its smaller population base rather than superior air quality.

**Statistical Significance and Limitations**  
With only five data points (boroughs) per pollutant, our correlation analysis has limited statistical power. The sample size precludes formal significance testing, and the results should be interpreted as exploratory rather than confirmatory. The borough-level aggregation, while necessary for data integration, obscures important within-borough variation in both pollution exposure and health outcomes. Additionally, ecological fallacy concerns apply—correlations observed at the borough level may not hold at the individual or neighborhood level.

**Visualization**  
The correlation heatmap (`docs/correlation.png`) provides a visual summary of these findings, displaying the three pollutants as rows with color intensity representing correlation strength. The gradient from cool (negative correlation) to warm (positive correlation) colors highlights ozone's distinctive stronger positive association compared to the other pollutants.

## Future Work
This project establishes a foundational framework for analyzing air quality and health relationships in New York City, but several important avenues for future research and methodological improvements have been identified through our work.

**Enhanced Spatial Resolution**: Our borough-level analysis, while useful for initial exploration, sacrifices significant spatial detail. Future work should improve the spatial join by mapping census block groups to finer geographic units such as Neighborhood Tabulation Areas (NTAs) or Community Districts. New York City's 195 NTAs would provide a middle ground between block groups and boroughs, offering sufficient granularity to capture neighborhood-level variation while maintaining adequate statistical power. This would enable identification of environmental justice concerns, where specific neighborhoods disproportionately bear pollution burdens. Implementing spatial joins could leverage GIS tools (e.g., geopandas, PostGIS) to perform proper geometric intersections rather than relying on FIPS code range assumptions. Additionally, incorporating spatial autocorrelation analysis (Moran's I, Geary's C) would reveal whether pollution and health impacts cluster geographically, informing targeted intervention strategies.

**Temporal Analysis and Time-Series Modeling**: Our current analysis aggregates data across time periods, masking important temporal dynamics. A comprehensive temporal analysis would examine: (1) **Seasonal Variation**: Air quality exhibits strong seasonal patterns—ozone peaks in summer due to photochemical reactions, while PM 2.5 often peaks in winter due to heating emissions and atmospheric inversion conditions. Analyzing these seasonal trends would improve causal inference; (2) **Longitudinal Trends**: New York City's air quality has generally improved over the past decades due to regulations like the Clean Air Act. Time-series analysis could quantify these improvements and correlate them with health outcome changes; (3) **Lag Effects**: Health impacts may not be instantaneous. Distributed lag models could examine whether pollution exposure in previous days, weeks, or months predicts current health outcomes; (4) **Event Studies**: Analyzing acute pollution episodes (e.g., wildfire smoke events, traffic pattern changes during COVID-19) could provide natural experiments for estimating causal health effects. Implementing ARIMA models, seasonal decomposition, or more sophisticated time-series methods would substantially strengthen the analytical rigor.

**Advanced Statistical Modeling**: Moving beyond simple correlation to multivariable regression models would control for confounding variables and enable causal inference. Key confounders to incorporate include: (1) **Population Characteristics**: Age structure, baseline health status, socioeconomic status, and healthcare access all influence health outcomes independent of pollution exposure; (2) **Built Environment**: Population density, proximity to green space, building density, and traffic volume; (3) **Meteorological Factors**: Temperature, humidity, and wind patterns affect both pollution concentrations and health outcomes; (4) **Multipollutant Models**: Pollutants co-occur and interact. Two-pollutant or multi-pollutant models could disentangle independent effects. Hierarchical models or mixed-effects models accounting for spatial clustering would be methodologically appropriate. Generalized Additive Models (GAMs) could capture non-linear dose-response relationships that linear correlation misses.

**Data Integration and Enrichment**: Several additional datasets could enrich the analysis: (1) **Socioeconomic Data**: American Community Survey (ACS) data on income, education, and race/ethnicity could enable environmental justice analysis; (2) **Land Use Data**: NYC's PLUTO dataset provides parcel-level land use information to characterize pollution sources; (3) **Traffic Data**: NYC DOT traffic volume data could improve NO2 source attribution; (4) **Hospital Records**: While the BenMAP data provides modeled estimates, linking to actual emergency department visit records or hospital admission data (if available and de-identified) would validate the models; (5) **Personal Exposure Monitoring**: Citizen science approaches using low-cost sensors could capture micro-scale pollution variation missed by regulatory monitors.

**Machine Learning Approaches**: Advanced machine learning methods could improve predictive power: (1) **Random Forests or Gradient Boosting**: These ensemble methods handle non-linear relationships and interactions better than linear models; (2) **Spatial Interpolation**: Kriging or machine learning-based interpolation (e.g., neural networks) could predict pollution at unmeasured locations; (3) **Causal Inference Methods**: Propensity score matching, instrumental variables, or difference-in-differences approaches could strengthen causal claims if appropriate quasi-experimental designs can be identified.

**Addressing Data Quality Limitations**: Future iterations should address the temporal misalignment between datasets by obtaining or generating contemporaneous health impact estimates. Collaborating with epidemiologists to develop updated BenMAP scenarios using recent air quality data would be valuable. Additionally, the PM 2.5 resuspension issue should be investigated further—potentially through sensitivity analyses that exclude negative values or through consultation with domain experts to understand whether aggregating positive and negative values is appropriate.

**Policy-Relevant Analysis**: To maximize impact, future work should focus on policy-relevant questions: (1) **Intervention Targeting**: Which neighborhoods would benefit most from air quality interventions? (2) **Health Co-Benefits**: What health benefits would accrue from specific policy scenarios (e.g., congestion pricing, truck route restrictions, green infrastructure)? (3) **Cost-Benefit Analysis**: Quantifying monetized health benefits could inform policy prioritization; (4) **Environmental Justice**: Are pollution burdens and health impacts equitably distributed across demographic groups?

**Reproducibility and Open Science**: While this project emphasizes reproducibility through automation scripts and documentation, future work could further embrace open science principles by: (1) Publishing to academic data repositories (e.g., Zenodo, figshare) with persistent DOIs; (2) Developing interactive web visualizations (e.g., Shiny apps, Plotly dashboards) for public engagement; (3) Contributing cleaned, integrated datasets back to public repositories; (4) Publishing findings in open-access journals or preprint servers.

**Methodological Lessons Learned**: This project revealed several practical lessons for data-intensive research: (1) **Early Data Profiling**: Investing time upfront in thorough data profiling prevented downstream errors; (2) **Iterative Development**: The multi-stage pipeline (inspect → load → clean → analyze) with intermediate checkpoints facilitated debugging; (3) **Documentation as You Go**: Maintaining parallel documentation while coding proved more effective than retrospective documentation; (4) **Version Control Best Practices**: Regular commits with descriptive messages enabled tracking progress and reverting errors; (5) **Automation Payoff**: Although creating the `run_all.py` script required extra effort, it dramatically improved reproducibility and saved time during final testing. These lessons will inform future data curation projects and could be shared as best practices for students and researchers undertaking similar work.

## Updated Timeline
*   **Milestone 1 - Team Selection (Sept 26):** Completed on time. Team formed with Kenneth Shelton and Tianqi Fu.
*   **Milestone 2 - Project Plan (Oct 7):** Completed on time. Defined research question, datasets, roles, and initial timeline.
*   **Milestone 3 - Interim Status Report (Nov 11):** Completed on time. Reported progress on data acquisition, SQL schema design, and initial quality assessment. Identified date format inconsistencies and negative PM2.5 values requiring attention.
*   **Milestone 4 - Final Project Submission (Dec 7):** Completed. Includes complete data pipeline, analysis, visualization, and comprehensive documentation.

### Project Execution Timeline
*   **October:** Data acquisition, checksum verification, initial profiling, and database schema design.
*   **Late October - November:** Data cleaning pipeline development. Addressed date format inconsistencies and PM2.5 resuspension values. Significant delays occurred due to the complexity of temporal data normalization and geographic aggregation decisions.
*   **Early December:** Data integration (borough-level aggregation using FIPS codes), correlation analysis, and visualization generation.
*   **December 5-7:** Final documentation, README expansion, metadata creation, and reproducibility package assembly.

## Project Plan Changes
1.  **Geographic Aggregation**: We originally planned complex spatial joins. We simplified this to FIPS-based aggregation (Block Group -> Borough) to ensure compatibility within the project timeframe.
2.  **Scope Reduction**: We focused specifically on "Acute Respiratory Symptoms" rather than all health outcomes to ensure a focused analysis.
3.  **Tooling**: We relied heavily on Python (pandas) for integration rather than SQL joins, as the data transformation (melting/pivoting) was more efficient in pandas.

## Reproducing
To reproduce our results:

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/KennethShelton/IS-477-Project.git
    cd IS-477-Project
    ```

2.  **Download the data** (if not included in repository):
    ```bash
    python scripts/download_data.py
    ```
    This will download both datasets and verify checksums.

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the full pipeline**:
    ```bash
    python scripts/run_all.py
    ```
    This script will:
    *   Inspect raw data (`docs/inspect_report.txt`).
    *   Load data into SQLite (`data/nyc_air_health.db`).
    *   Clean and normalize data (`data/processed/*_clean.csv`).
    *   Run the analysis and generate outputs:
        - `data/processed/merged.csv` (integrated dataset)
        - `docs/correlation.png` (correlation heatmap)

For detailed workflow documentation, see `docs/WORKFLOW.md`.  
For data structure details, see `docs/DATA_DICTIONARY.md`.

**Note**: Large data files (`data/nyc_air_health.db`, `data/raw/air_quality.csv`, `data/raw/NYNY_BenMAP.csv`, and `data/processed/*`) are available via Box: [INSERT BOX LINK HERE]

## Licenses
*   **Software**: This project's code is released under the MIT License. See `LICENSE` for details.
*   **Data**: Source data is public domain. Derived data is released under CC0 1.0. See `DATA_LICENSE.md` for details.

## References
1.  New York City Air Quality. (n.d.). Retrieved from https://catalog.data.gov/dataset/air-quality
2.  EnviroAtlas New York City - BenMAP Results. (n.d.). Retrieved from https://catalog.data.gov/dataset/enviroatlas-new-york-city-ny-benmap-results-by-block-group3
3.  pandas development team. (2020). pandas-dev/pandas: Pandas (v1.5.0). Zenodo. https://doi.org/10.5281/zenodo.3509134
4.  Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. Computing in Science & Engineering, 9(3), 90-95.
5.  Waskom, M. L. (2021). seaborn: statistical data visualization. Journal of Open Source Software, 6(60), 3021.
