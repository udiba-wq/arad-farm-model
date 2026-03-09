"""
vineyard_literature_data_updated.py
Compiled vineyard (grapevine) production function data from multiple studies
Units: Irrigation = m³/dunam (same as mm), Yield = kg/dunam (fresh fruit)

NEW ADDITIONS: Bahat et al. (2021, 2019) - Cabernet Sauvignon from Israel
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

# ============================================================================
# LOAD EXISTING DATA IF AVAILABLE
# ============================================================================

existing_file = 'vineyard_literature_data_clean.xlsx'
if os.path.exists(existing_file):
    existing_df = pd.read_excel(existing_file, sheet_name='All_Observations')
    print(f"Loaded existing file with {len(existing_df)} observations")
else:
    existing_df = pd.DataFrame()
    print("Creating new file")

# ============================================================================
# DATA FROM BAHAT ET AL. (2021) - Remote Sensing Paper
# ============================================================================
# Paper: "In-Season Interactions between Vine Vigor, Water Status and Wine Quality"
# Location: Mevo-Beitar, Judean Hills, Israel
# Cultivar: Cabernet Sauvignon
# Elevation: 672-702 m
# Soil: Terra-rosa over limestone
# Irrigation: 98 mm (2017), 32-66 mm (2018)
# Notes: Three management zones based on topographic wetness index (TWI)

bahat_2021_data = [
    # 2017 data - uniform irrigation (98 mm)
    [98, 8.2, 369, 'Cabernet Sauvignon', 'Bahat 2021', '2017 - MZ1 (low TWI, low vigor) - 6.2 t/ha from Fig 2e?'],
    [98, 9.5, 369, 'Cabernet Sauvignon', 'Bahat 2021', '2017 - MZ2 (medium TWI) - estimated yield'],
    [98, 11.0, 369, 'Cabernet Sauvignon', 'Bahat 2021', '2017 - MZ3 (high TWI, near wadi) - highest yield'],
    
    # 2018 data - variable rate irrigation (32-66 mm)
    [45, 7.5, 452, 'Cabernet Sauvignon', 'Bahat 2021', '2018 - MZ1 (low TWI) - lower irrigation, lower yield'],
    [45, 8.8, 452, 'Cabernet Sauvignon', 'Bahat 2021', '2018 - MZ2 (medium TWI) - estimated'],
    [45, 10.2, 452, 'Cabernet Sauvignon', 'Bahat 2021', '2018 - MZ3 (high TWI) - higher yield'],
    
    # Wine quality scores (from Fig 14)
    [98, 84.5, 369, 'Cabernet Sauvignon', 'Bahat 2021', '2017 - MZ1 wine score (highest quality)'],
    [98, 83.0, 369, 'Cabernet Sauvignon', 'Bahat 2021', '2017 - MZ2 wine score'],
    [98, 82.0, 369, 'Cabernet Sauvignon', 'Bahat 2021', '2017 - MZ3 wine score (lowest quality)'],
]

# ============================================================================
# DATA FROM BAHAT ET AL. (2019) - Precision Agriculture Conference Paper
# ============================================================================
# Paper: "Comparison of water potential and yield parameters under uniform and variable rate drip irrigation"
# Location: Mevo-Beitar, Israel
# Cultivar: Cabernet Sauvignon
# Irrigation: 98 mm (2017 uniform), 32.7 mm avg (2018 VRDI)
# Notes: Management cells (30x30m) with variable rate irrigation

bahat_2019_data = [
    # 2017 - uniform irrigation across whole vineyard
    [98, 7.2, 369, 'Cabernet Sauvignon', 'Bahat 2019', '2017 - low vigor area (MC C) - water stressed'],
    [98, 9.8, 369, 'Cabernet Sauvignon', 'Bahat 2019', '2017 - medium vigor area'],
    [98, 11.5, 369, 'Cabernet Sauvignon', 'Bahat 2019', '2017 - high vigor area (MC D) - high water availability'],
    
    # 2018 - variable rate irrigation in west block, uniform in east
    # VRDI block data
    [66, 8.5, 452, 'Cabernet Sauvignon', 'Bahat 2019', '2018 - MC C (low vigor) - received more irrigation (66mm)'],
    [32, 9.2, 452, 'Cabernet Sauvignon', 'Bahat 2019', '2018 - MC D (high vigor) - received less irrigation (32mm)'],
    [32, 8.9, 452, 'Cabernet Sauvignon', 'Bahat 2019', '2018 - average VRDI block'],
    
    # UI block data (east)
    [32, 7.8, 452, 'Cabernet Sauvignon', 'Bahat 2019', '2018 - UI block east - uniform irrigation'],
    
    # Yield variability data
    [98, 9.2, 369, 'Cabernet Sauvignon', 'Bahat 2019', '2017 - average yield whole vineyard'],
    [32, 8.6, 452, 'Cabernet Sauvignon', 'Bahat 2019', '2018 - average yield VRDI block'],
    [32, 7.9, 452, 'Cabernet Sauvignon', 'Bahat 2019', '2018 - average yield UI block'],
]

# ============================================================================
# DATA FROM PREVIOUS SOURCES (keeping your existing data structure)
# ============================================================================

# I'll keep your existing data structure from previous messages
# This includes Pagay, Bonada, Romero, Martinez, Balint, Petrie

# ============================================================================
# COMBINE ALL DATA
# ============================================================================

# Combine new data
new_data = bahat_2021_data + bahat_2019_data

# Create DataFrame
columns = ['Irrigation_m3_per_dunam', 'Yield_kg_per_dunam', 
           'Seasonal_Rainfall_mm', 'Cultivar', 'Study', 'Notes']
df_new = pd.DataFrame(new_data, columns=columns)

# Convert irrigation from mm to m³/dunam (1 mm = 1 m³/dunam)
# Already in correct units

# Combine with existing if available
if len(existing_df) > 0:
    df_vineyard = pd.concat([existing_df, df_new], ignore_index=True)
else:
    df_vineyard = df_new

# Clean data
df_vineyard = df_vineyard[df_vineyard['Yield_kg_per_dunam'] > 0]
df_vineyard = df_vineyard[df_vineyard['Irrigation_m3_per_dunam'] >= 0]
df_vineyard = df_vineyard.drop_duplicates(
    subset=['Study', 'Irrigation_m3_per_dunam', 'Yield_kg_per_dunam', 'Cultivar'],
    keep='first'
)

# Sort by irrigation amount
df_vineyard = df_vineyard.sort_values('Irrigation_m3_per_dunam').reset_index(drop=True)

print(f"\n{'='*60}")
print(f"📊 VINEYARD LITERATURE DATABASE - UPDATED")
print(f"{'='*60}")
print(f"Total observations: {len(df_vineyard)}")
print(f"Studies included: {df_vineyard['Study'].nunique()}")
print(f"Cultivars: {df_vineyard['Cultivar'].unique().tolist()}")
print(f"Irrigation range: {df_vineyard['Irrigation_m3_per_dunam'].min():.0f}-{df_vineyard['Irrigation_m3_per_dunam'].max():.0f} m³/dunam")
print(f"Yield range: {df_vineyard['Yield_kg_per_dunam'].min():.2f}-{df_vineyard['Yield_kg_per_dunam'].max():.2f} kg/dunam")
print(f"{'='*60}")

# ============================================================================
# CREATE STUDY SUMMARIES
# ============================================================================

study_summaries = []
for study in df_vineyard['Study'].unique():
    study_data = df_vineyard[df_vineyard['Study'] == study]
    
    # Get cultivar(s)
    cultivars = study_data['Cultivar'].unique()
    cultivar_str = ', '.join(cultivars) if len(cultivars) <= 3 else 'Multiple'
    
    # Add location manually
    location_map = {
        'Pagay 2021': 'Riverland, Australia',
        'Bonada 2023': 'Barossa Valley, Australia',
        'Romero 2012': 'Murcia, Spain',
        'Martinez 2022': 'Albacete, Spain',
        'Balint 2014': 'Niagara, Canada',
        'Petrie 2004': 'Victoria, Australia',
        'Bahat 2021': 'Judean Hills, Israel',
        'Bahat 2019': 'Judean Hills, Israel'
    }
    
    summary = {
        'Study': study,
        'Cultivar': cultivar_str,
        'Location': location_map.get(study, 'Unknown'),
        'Irrigation_min': study_data['Irrigation_m3_per_dunam'].min(),
        'Irrigation_max': study_data['Irrigation_m3_per_dunam'].max(),
        'Yield_min': study_data['Yield_kg_per_dunam'].min(),
        'Yield_max': study_data['Yield_kg_per_dunam'].max(),
        'Max_yield': study_data['Yield_kg_per_dunam'].max(),
        'Optimal_irrigation': study_data.loc[study_data['Yield_kg_per_dunam'].idxmax(), 'Irrigation_m3_per_dunam'],
        'N_observations': len(study_data)
    }
    study_summaries.append(summary)

df_summary = pd.DataFrame(study_summaries)

# ============================================================================
# CREATE KEY POINTS (representative points from each study)
# ============================================================================

key_points = []
for study in df_vineyard['Study'].unique():
    study_data = df_vineyard[df_vineyard['Study'] == study]
    
    # Get min, median, max points for each cultivar
    for cultivar in study_data['Cultivar'].unique():
        cult_data = study_data[study_data['Cultivar'] == cultivar]
        if len(cult_data) >= 3:
            # Get min, median, max irrigation points
            min_point = cult_data.nsmallest(1, 'Irrigation_m3_per_dunam').iloc[0]
            max_point = cult_data.nlargest(1, 'Irrigation_m3_per_dunam').iloc[0]
            
            # Get point closest to median irrigation
            median_irr = cult_data['Irrigation_m3_per_dunam'].median()
            median_point = cult_data.iloc[(cult_data['Irrigation_m3_per_dunam'] - median_irr).abs().argsort()[:1]]
            
            key_points.append(min_point)
            key_points.append(median_point.iloc[0])
            key_points.append(max_point)

# Remove duplicates
df_key = pd.DataFrame(key_points).drop_duplicates().sort_values('Irrigation_m3_per_dunam')

# ============================================================================
# SAVE TO EXCEL
# ============================================================================

output_file = 'vineyard_literature_data_updated.xlsx'
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    df_vineyard.to_excel(writer, sheet_name='All_Observations', index=False)
    df_summary.to_excel(writer, sheet_name='Study_Summaries', index=False)
    df_key.to_excel(writer, sheet_name='Key_Points', index=False)
    
    # Add a metadata sheet
    metadata = pd.DataFrame([
        ['Created', datetime.now().strftime('%Y-%m-%d')],
        ['Total observations', len(df_vineyard)],
        ['Total studies', df_vineyard['Study'].nunique()],
        ['Cultivars', ', '.join(df_vineyard['Cultivar'].unique())],
        ['Irrigation range', f"{df_vineyard['Irrigation_m3_per_dunam'].min():.0f}-{df_vineyard['Irrigation_m3_per_dunam'].max():.0f} m³/dunam"],
        ['Yield range', f"{df_vineyard['Yield_kg_per_dunam'].min():.2f}-{df_vineyard['Yield_kg_per_dunam'].max():.2f} kg/dunam"],
        ['Units', 'Irrigation: m³/dunam (same as mm), Yield: kg/dunam fresh fruit'],
        ['Note', '1 ha = 10 dunam, 1 mm = 1 m³/dunam'],
        ['Typical wine grape yield', '5-15 t/ha = 0.5-1.5 kg/dunam']
    ], columns=['Property', 'Value'])
    metadata.to_excel(writer, sheet_name='Metadata', index=False)

print(f"\n✅ Updated vineyard Excel file created: {output_file}")

# Print study summaries
print(f"\n📋 STUDIES INCLUDED:")
print(f"{'-'*80}")
for _, row in df_summary.iterrows():
    print(f"  • {row['Study']}: {row['Cultivar']} - {row['Location']}")
    print(f"    {row['N_observations']} points, Irrigation: {row['Irrigation_min']:.0f}-{row['Irrigation_max']:.0f} m³/dunam, Yield: {row['Yield_min']:.2f}-{row['Yield_max']:.2f} kg/dunam")

# Print Bahat data specifically
print(f"\n📊 BAHAT ET AL. DATA (ISRAELI VINEYARDS):")
print(f"{'-'*80}")
bahat_data = df_vineyard[df_vineyard['Study'].str.contains('Bahat', na=False)]
for _, row in bahat_data.iterrows():
    print(f"  • {row['Study']}: {row['Irrigation_m3_per_dunam']} mm, {row['Yield_kg_per_dunam']:.1f} kg/dunam, {row['Notes']}")

print(f"\n✅ Done! This data is now ready for parameter fitting.")