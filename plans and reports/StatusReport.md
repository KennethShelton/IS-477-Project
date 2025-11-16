# Status Report

## Tianqi’s Portion:

## Kenneth’s Portion: City of New York Air Quality Dataset Notes

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

