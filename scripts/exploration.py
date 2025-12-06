import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns

#Load air_quality_clean.csv
aq_clean_path=os.path.join('data', 'processed', 'air_quality_clean.csv')
df_air=pd.read_csv(os.path.abspath(aq_clean_path))

#Separate by borough
df_air_bronx=df_air[df_air['Geo Place Name']=='Bronx']
df_air_brooklyn=df_air[df_air['Geo Place Name'] == 'Brooklyn']
df_air_manhattan=df_air[df_air['Geo Place Name']=='Manhattan']
df_air_queens=df_air[df_air['Geo Place Name']=='Queens']
df_air_staten=df_air[df_air['Geo Place Name']=='Staten Island']

#Select PM 2.5 data from boroughs
df_air_bronx_pm=df_air_bronx[(df_air_bronx['Name']=='Fine particles (PM 2.5)')&(df_air_bronx['Time Period'].str.contains('Annual Average'))].sort_values(by='year')
df_air_brooklyn_pm=df_air_brooklyn[(df_air_brooklyn['Name']=='Fine particles (PM 2.5)')&(df_air_brooklyn['Time Period'].str.contains('Annual Average'))].sort_values(by='year')
df_air_manhattan_pm=df_air_manhattan[(df_air_manhattan['Name']=='Fine particles (PM 2.5)')&(df_air_manhattan['Time Period'].str.contains('Annual Average'))].sort_values(by='year')
df_air_queens_pm=df_air_queens[(df_air_queens['Name']=='Fine particles (PM 2.5)')&(df_air_queens['Time Period'].str.contains('Annual Average'))].sort_values(by='year')
df_air_staten_pm=df_air_staten[(df_air_staten['Name']=='Fine particles (PM 2.5)')&(df_air_staten['Time Period'].str.contains('Annual Average'))].sort_values(by='year')

#Plot average PM 2.5 by borough per year
plt.plot(df_air_bronx_pm['year'], df_air_bronx_pm['Data Value'])
plt.plot(df_air_brooklyn_pm['year'], df_air_brooklyn_pm['Data Value'])
plt.plot(df_air_manhattan_pm['year'], df_air_manhattan_pm['Data Value'])
plt.plot(df_air_queens_pm['year'], df_air_queens_pm['Data Value'])
plt.plot(df_air_staten_pm['year'], df_air_staten_pm['Data Value'])
plt.axhline(y=9, color='black', linestyle='--')
plt.legend(['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island', 'National Standard'])
plt.locator_params(axis='x', nbins=16)
plt.xticks(rotation=45)
plt.title("Average PM 2.5 in NYC Boroughs per Year")
plt.xlabel('Year')
plt.ylabel('Mean PM 2.5 (mcg/m3)')
plt.savefig('pm25.png')
plt.show()

#Select NO2 data from boroughs
df_air_bronx_no2=df_air_bronx[(df_air_bronx['Name']=='Nitrogen dioxide (NO2)')&(df_air_bronx['Time Period'].str.contains('Annual Average'))].sort_values(by='year')
df_air_brooklyn_no2=df_air_brooklyn[(df_air_brooklyn['Name']=='Nitrogen dioxide (NO2)')&(df_air_brooklyn['Time Period'].str.contains('Annual Average'))].sort_values(by='year')
df_air_manhattan_no2=df_air_manhattan[(df_air_manhattan['Name']=='Nitrogen dioxide (NO2)')&(df_air_manhattan['Time Period'].str.contains('Annual Average'))].sort_values(by='year')
df_air_queens_no2=df_air_queens[(df_air_queens['Name']=='Nitrogen dioxide (NO2)')&(df_air_queens['Time Period'].str.contains('Annual Average'))].sort_values(by='year')
df_air_staten_no2=df_air_staten[(df_air_staten['Name']=='Nitrogen dioxide (NO2)')&(df_air_staten['Time Period'].str.contains('Annual Average'))].sort_values(by='year')

#Plot average NO2 by borough per year
plt.plot(df_air_bronx_no2['year'], df_air_bronx_no2['Data Value'])
plt.plot(df_air_brooklyn_no2['year'], df_air_brooklyn_no2['Data Value'])
plt.plot(df_air_manhattan_no2['year'], df_air_manhattan_no2['Data Value'])
plt.plot(df_air_queens_no2['year'], df_air_queens_no2['Data Value'])
plt.plot(df_air_staten_no2['year'], df_air_staten_no2['Data Value'])
plt.legend(['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island', 'National Standard'])
plt.locator_params(axis='x', nbins=16)
plt.xticks(rotation=45)
plt.title("Average Nitrogen Dioxide in NYC Boroughs per Year")
plt.xlabel('Year')
plt.ylabel('Mean NO2 (ppb)')
plt.savefig('no2.png')
plt.show()

#Select ozone data from boroughs
df_air_bronx_o3=df_air_bronx[(df_air_bronx['Name']=='Ozone (O3)')&(df_air_bronx['Time Period'])].sort_values(by='year')
df_air_brooklyn_o3=df_air_brooklyn[(df_air_brooklyn['Name']=='Ozone (O3)')&(df_air_brooklyn['Time Period'])].sort_values(by='year')
df_air_manhattan_o3=df_air_manhattan[(df_air_manhattan['Name']=='Ozone (O3)')&(df_air_manhattan['Time Period'])].sort_values(by='year')
df_air_queens_o3=df_air_queens[(df_air_queens['Name']=='Ozone (O3)')&(df_air_queens['Time Period'])].sort_values(by='year')
df_air_staten_o3=df_air_staten[(df_air_staten['Name']=='Ozone (O3)')&(df_air_staten['Time Period'])].sort_values(by='year')

#Plot average ozone by borough per year
plt.plot(df_air_bronx_o3['year'], df_air_bronx_o3['Data Value'])
plt.plot(df_air_brooklyn_o3['year'], df_air_brooklyn_o3['Data Value'])
plt.plot(df_air_manhattan_o3['year'], df_air_manhattan_o3['Data Value'])
plt.plot(df_air_queens_o3['year'], df_air_queens_o3['Data Value'])
plt.plot(df_air_staten_o3['year'], df_air_staten_o3['Data Value'])
plt.legend(['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island', 'National Standard'])
plt.locator_params(axis='x', nbins=16)
plt.xticks(rotation=45)
plt.title("Average Ozone in NYC Boroughs per Year")
plt.xlabel('Year')
plt.ylabel('Mean O3 (ppb)')
plt.savefig('ozone.png')
plt.show()

#Load NYNY_BenMAP_clean.csv
ben_clean_path=os.path.join('data', 'processed', 'NYNY_BenMAP_clean.csv')
df_ben=pd.read_csv(os.path.abspath(ben_clean_path))

#Select desired columns
df_ben_a=df_ben[['bgrp', 'NO2_Acute_Respiratory_Symptoms_I', 'O3_Acute_Respiratory_Symptoms_I', 'PM25_Acute_Respiratory_Symptoms_I']]

#Add borough column
def get_borough_from_bgrp(bgrp):
    if 360050000000 <= bgrp <= 360059999999:
        return 'Bronx'
    elif 360470000000 <= bgrp <= 360479999999:
        return 'Brooklyn'
    elif 360610000000 <= bgrp <= 360619999999:
        return 'Manhattan'
    elif 360810000000 <= bgrp <= 360819999999:
        return 'Queens'
    elif 360850000000 <= bgrp <= 360859999999:
        return 'Staten Island'

df_ben_b=df_ben_a.copy()
df_ben_b['Borough'] = df_ben_b['bgrp'].apply(get_borough_from_bgrp)

#Reorder columns after adding 'Borough'
ben_new_order=['bgrp', 'Borough', 'NO2_Acute_Respiratory_Symptoms_I', 'O3_Acute_Respiratory_Symptoms_I', 'PM25_Acute_Respiratory_Symptoms_I']
df_ben_b=df_ben_b[ben_new_order]

#Sum incidences by borough
no_brgp=['Borough', 'NO2_Acute_Respiratory_Symptoms_I', 'O3_Acute_Respiratory_Symptoms_I', 'PM25_Acute_Respiratory_Symptoms_I']
df_ben_b_group=df_ben_b[no_brgp].groupby('Borough').sum().reset_index()

#Plot acute respiratory symptoms by pollutant and borough
df_melted = df_ben_b_group.melt(id_vars=['Borough'],
                                 value_vars=['NO2_Acute_Respiratory_Symptoms_I',
                                             'PM25_Acute_Respiratory_Symptoms_I',
                                             'O3_Acute_Respiratory_Symptoms_I'],
                                 var_name='Pollutant', value_name='Incidences')

df_melted['Pollutant'] = df_melted['Pollutant'].map({
    'NO2_Acute_Respiratory_Symptoms_I': 'NO2',
    'O3_Acute_Respiratory_Symptoms_I': 'O3',
    'PM25_Acute_Respiratory_Symptoms_I': 'PM2.5'
})

pollutant_order = ['NO2', 'PM2.5', 'O3']
df_melted['Pollutant'] = pd.Categorical(df_melted['Pollutant'], categories=pollutant_order, ordered=True)

fig, ax = plt.subplots(figsize=(12, 7))

sns.barplot(x='Pollutant', y='Incidences', hue='Borough', data=df_melted, ax=ax)

ax.set_ylabel('Number of Incidences')
ax.set_title('Acute Respiratory Symptoms by Pollutant and Borough')
ax.set_xlabel('Pollutant')
ax.legend(title='Borough')

for container in ax.containers:
    ax.bar_label(container, fmt='%d', padding=3)

fig.tight_layout()
plt.savefig('respiratory.png')
plt.show()