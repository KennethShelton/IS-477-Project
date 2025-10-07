Kenneth Shelton & Tianqi Fu  
IS 477  
October 6, 2025

# Overview and Research Question

The goal of this project is to measure the relationship between the amount of air pollution in New York City and the health of New Yorkers. More specifically, which air pollutants are most prevalent in New York City, where are they most prevalent, and how many New Yorkers in those areas are suffering from health conditions possibly related to that pollution?

# Team Roles

Tianqi will be in charge of data collection and verification, meaning they will ensure the data’s integrity with a checksum and document the collection and verification process. They will also be responsible for the storage of that data through SQL, documenting the scripts, filesystem structure, and naming convention. Then they will integrate that SQL database into Python and document their process and queries. They will clean the data as well, making sure to note their operation history.

Kenneth will be in charge of data analysis, visualization, and documenting both. They will create a workflow and document the steps it took to make it. They will also ensure anyone can reproduce the project by verifying everything necessary is documented and output data is shared, specifying software dependencies, and creating licenses for the project. They must also upload a data dictionary and make descriptive metadata.

# Data

### [New York City Air Quality](https://catalog.data.gov/dataset/air-quality)

Description: It contains measures of various types of air pollutants, vehicle miles traveled, and health issues reported in New York City based on location, which are referred to as indicators.

Source: The New York City government.

Columns names and definitions:

* Unique ID: The unique record identifier.  
  * Example: 336867  
* Indicator ID: An identifier of the type of measured indicator.  
  * Example: 375  
* Name: The name of the indicator.  
  * Examples: Nitrogen dioxide, asthma emergency department visits due to PM2.5, and annual vehicle miles traveled.  
* Measure: How the indicator is measured.  
  * Example: Mean  
* Measure Info: Information (such as units) about the measure.  
  * Example: ppb  
* Geo Type Name: The geography type measured.  
  * Example: Citywide  
* Geo Join ID: An identifier of the neighborhood geographic area, used for joining to mapping geography files to make thematic maps.  
  * Ex: 407  
* Geo Place Name: The neighborhood name.  
  * Example: Upper West Side (CD7)  
* Time Period: A description of the time that the data applies to.  
  * Example: Winter 2014-15  
* Start\_Date: The date value for the start of the time period.  
  * Example: 12/01/2014  
* Data Value: The data value for the indicator, measure, place, and time.  
  * Example: 27.42  
* Message: Notes that apply to the data value (very few examples).

### [EnviroAtlas New York City](https://catalog.data.gov/dataset/enviroatlas-new-york-city-ny-benmap-results-by-block-group3)

Description: It records the effect of changes in pollution concentration on local populations in 6,378 block groups in New York City. 

Source: The USDA Forest Service, with support from the Davey Tree Expert Company.

Column names and definitions (not a list of every column included in the dataset, and all listed are numeric):

* bgrp: The census block group identifier; a concatenation of 2010 Census state FIPS code, county FIPS code, census tract code, and block group number.  
* NO2\_Hospital Admissions\_I: Incidence of hospital admissions due to a change in NO2 concentration.  
* NO2\_Emergency Room Visits\_I: Incidence of emergency room visits due to a change in NO2 concentration.  
* O3\_Hospital Admissions\_I: Incidence of hospital admissions due to a change in O3 concentration  
* O3\_Emergency Room Visits\_I: Incidence of emergency room visits due to a change in O3 concentration.  
* O3\_Mortality\_I: Incidence of mortality due to a change in O3 concentration.  
* PM25\_Hospital Admissions, Cardiovascular\_I: Incidence of hospital admissions (cardiovascular) due to a change in PM2.5 concentration. Negative values indicate resuspension of particles.  
* PM25\_Hospital Admissions, Respiratory\_I: Incidence of hospital admissions (respiratory) due to a change in PM2.5 concentration. Negative values indicate resuspension of particles.  
* PM25\_Emergency Room Visits\_I: Incidence of emergency room visits due to change in PM2.5 concentration. Negative values indicate resuspension of particles.  
* PM25\_Mortality\_I: Incidence of mortality due to a change in PM2.5 concentration. Negative values indicate resuspension of particles.  
* SO2\_Hospital Admissions\_I: Incidence of hospital admissions due to a change in SO2 concentration.  
* SO2\_Emergency Room Visits\_I: Incidence of emergency room visits due to a change in SO2 concentration.

# Timeline

**Phase 0 (Setup & Scope Clarification, Oct 7–Oct 9):** Immediately confirm the final version of datasets we will use, agree on research questions, define directory structure and naming conventions, and outline deliverables and dependencies.

**Phase 1 (Data Integration & Cleaning, Oct 10–Oct 16):** Tianqi will build the SQL schema, ingest all raw datasets, run checksum validations, clean missing or anomalous values, and perform spatial joins or geographic matching so we have a clean, integrated dataset ready for analysis.

**Phase 2 (Exploratory Analysis & Visualization, Oct 17–Oct 23):** Kenneth will compute descriptive statistics of pollutant levels across time and geography, map pollutant concentrations, overlay health indicator estimates, produce correlation matrices or scatterplots, and generate initial maps to visualize spatial patterns.

**Phase 3 (Modeling & Validation, Oct 24–Oct 30):** Kenneth (with data support from Tianqi) will run regression or spatial models, validate residuals and assumptions, test robustness (e.g. sensitivity to inclusion/exclusion of outliers), and refine model specification.

**Phase 4 (Draft Report Writing, Oct 31–Nov 4):** Both members will collaboratively draft the report, writing the introduction, methods, results, discussion, and inserting visualizations and tables.

# Constraints

Several constraints are anticipated: (1) Geographic granularity mismatch—for example, the air quality data may use a broader neighborhood identifier than the health estimates, which are at the block group; (2) data for some pollutants or times may be incomplete or missing; (3) negative or "resuspension" values in PM2.5 health effect data, which may complicate interpretation; and (4) limited time–any delays in the beginning phases can jeopardize the schedule.

# Gap

It still needs to be checked whether the two datasets are in compatible coordinate reference systems or if they require reprojection. We also need to confirm which health indicators overlap or exactly match from one dataset to another, for the joining to be valid. We have yet to decide on the best modeling approach (ordinary regression, spatial econometrics, or multilevel models).

