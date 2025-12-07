import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
import sys

def run_analysis():
    print("Starting analysis...")
    
    # Define paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data', 'processed')
    aq_clean_path = os.path.join(data_dir, 'air_quality_clean.csv')
    ben_clean_path = os.path.join(data_dir, 'NYNY_BenMAP_clean.csv')
    output_csv_path = os.path.join(data_dir, 'merged.csv')
    output_plot_path = os.path.join(base_dir, 'docs', 'correlation.png')

    # Check if files exist
    if not os.path.exists(aq_clean_path) or not os.path.exists(ben_clean_path):
        print(f"Error: Input files not found in {data_dir}. Run clean_data.py first.")
        return

    # Load clean datasets
    print(f"Loading {aq_clean_path}...")
    df_air = pd.read_csv(aq_clean_path)
    print(f"Loading {ben_clean_path}...")
    df_ben = pd.read_csv(ben_clean_path)

    # --- Process Air Quality Data ---
    print("Processing Air Quality data...")
    # Select boroughs
    if 'Geo Type Name' in df_air.columns:
        df_air_borough = df_air[df_air['Geo Type Name'] == 'Borough']
    else:
        print("Warning: 'Geo Type Name' column not found. Using full dataset.")
        df_air_borough = df_air

    # Select rows with NO2, O3, and PM 2.5
    target_pollutants = ['Nitrogen dioxide (NO2)', 'Ozone (O3)', 'Fine particles (PM 2.5)']
    df_air_borough_a = df_air_borough[df_air_borough['Name'].isin(target_pollutants)]

    # Prepare columns for grouping
    # Note: 'Measure Info' might be needed for uniqueness, but we'll group by it too
    cols_to_keep = ['Indicator ID', 'Name', 'Measure Info', 'Geo Place Name', 'Data Value']
    # Ensure columns exist
    cols_to_keep = [c for c in cols_to_keep if c in df_air_borough_a.columns]
    df_air_borough_b = df_air_borough_a[cols_to_keep]

    # Group by Borough and Pollutant to get mean values
    # We group by Indicator ID, Name, Measure Info, Geo Place Name
    group_cols = ['Indicator ID', 'Name', 'Measure Info', 'Geo Place Name']
    group_cols = [c for c in group_cols if c in df_air_borough_b.columns]
    
    df_air_borough_b_group = df_air_borough_b.groupby(group_cols)['Data Value'].mean().reset_index()
    df_air_borough_b_group = df_air_borough_b_group.sort_values('Geo Place Name')

    # --- Process BenMAP Data ---
    print("Processing BenMAP data...")
    # Select desired columns
    ben_cols = ['bgrp', 'NO2_Acute_Respiratory_Symptoms_I', 'O3_Acute_Respiratory_Symptoms_I', 'PM25_Acute_Respiratory_Symptoms_I']
    df_ben_a = df_ben[ben_cols].copy()

    # Add borough column based on FIPS codes (bgrp)
    def get_borough_from_bgrp(bgrp):
        try:
            bgrp_val = int(bgrp)
            if 360050000000 <= bgrp_val <= 360059999999:
                return 'Bronx'
            elif 360470000000 <= bgrp_val <= 360479999999:
                return 'Brooklyn'
            elif 360610000000 <= bgrp_val <= 360619999999:
                return 'Manhattan'
            elif 360810000000 <= bgrp_val <= 360819999999:
                return 'Queens'
            elif 360850000000 <= bgrp_val <= 360859999999:
                return 'Staten Island'
        except:
            return None
        return None

    df_ben_a['Borough'] = df_ben_a['bgrp'].apply(get_borough_from_bgrp)

    # Sum incidences by borough
    df_ben_b_group = df_ben_a.groupby('Borough')[['NO2_Acute_Respiratory_Symptoms_I', 'O3_Acute_Respiratory_Symptoms_I', 'PM25_Acute_Respiratory_Symptoms_I']].sum().reset_index()

    # Prepare for integration (Melt)
    df_ben_melted = pd.melt(df_ben_b_group, id_vars=['Borough'],
                            value_vars=['NO2_Acute_Respiratory_Symptoms_I', 'O3_Acute_Respiratory_Symptoms_I', 'PM25_Acute_Respiratory_Symptoms_I'],
                            var_name='Symptom Type', value_name='Symptom Value')
    df_ben_melted = df_ben_melted.rename(columns={'Borough': 'Geo Place Name'})

    symptom_name_mapping = {
        'NO2_Acute_Respiratory_Symptoms_I': 'Nitrogen dioxide (NO2)',
        'O3_Acute_Respiratory_Symptoms_I': 'Ozone (O3)',
        'PM25_Acute_Respiratory_Symptoms_I': 'Fine particles (PM 2.5)'
    }
    df_ben_melted['Name'] = df_ben_melted['Symptom Type'].map(symptom_name_mapping)

    # --- Integration ---
    print("Merging datasets...")
    df_merged = pd.merge(df_air_borough_b_group, df_ben_melted, on=['Geo Place Name', 'Name'], how='inner')
    
    # Select and rename columns
    final_cols = ['Geo Place Name', 'Indicator ID', 'Name', 'Measure Info', 'Data Value', 'Symptom Type', 'Symptom Value']
    final_cols = [c for c in final_cols if c in df_merged.columns]
    df_merged = df_merged[final_cols].sort_values(['Geo Place Name', 'Symptom Type']).reset_index(drop=True)
    df_merged = df_merged.rename(columns={'Data Value': 'Mean Measure Value'})
    
    print(f"Saving merged data to {output_csv_path}...")
    df_merged.to_csv(output_csv_path, index=False)

    # --- Analysis & Visualization ---
    print("Calculating correlations...")
    correlations = {}
    for pollutant in target_pollutants:
        subset = df_merged[df_merged['Name'] == pollutant]
        if not subset.empty:
            corr = subset['Mean Measure Value'].corr(subset['Symptom Value'])
            correlations[pollutant] = corr
        else:
            correlations[pollutant] = None
    
    print("Correlations:", correlations)

    correlations_df = pd.DataFrame.from_dict(correlations, orient='index', columns=['Correlation'])
    
    print(f"Generating heatmap to {output_plot_path}...")
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlations_df, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Relationship between Air Pollutants and Acute Respiratory Symptoms')
    plt.tight_layout()
    plt.savefig(output_plot_path)
    print("Analysis complete.")

if __name__ == "__main__":
    run_analysis()
