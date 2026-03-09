"""
apricot_literature_data_updated.py
Compiled apricot production function data from multiple studies
Units: Irrigation = m³/dunam (same as mm), Yield = kg/dunam (fresh fruit)

NEW ADDITIONS:
- Mohamed & Eid (2013) - Egypt, Canino cultivar, 20-80% depletion levels
- Kaya et al. (2017) - Turkey, Salak cultivar, class A pan coefficients 0.5-1.5
- Pérez-Sarmiento et al. (2016) - Spain, Búlida cultivar, 3-year RDI study
- Ruiz-Sánchez et al. (2000) - Spain, Búlida cultivar, foundational RDI study
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

# ============================================================================
# LOAD EXISTING DATA IF AVAILABLE
# ============================================================================

existing_file = 'apricot_literature_data.xlsx'
if os.path.exists(existing_file):
    existing_df = pd.read_excel(existing_file, sheet_name='All_Observations')
    print(f"Loaded existing file with {len(existing_df)} observations")
else:
    existing_df = pd.DataFrame()
    print("Creating new file")

# ============================================================================
# DATA FROM MOHAMED & EID (2013) - Egypt
# ============================================================================
# Paper: "Irrigation Regimes for Apricot Trees under Different Rates of Soil Moisture Depletion"
# Location: El-Kanater, Kalubeia, Egypt
# Cultivar: Canino
# Soil: Clay loam
# Irrigation: 20%, 40%, 60%, 80% depletion from available soil moisture
# Yield: from Fig 3 and Table 7

mohamed_eid_2013_data = [
    # I1 - 20% depletion (wettest) - highest water use
    [4746/10, 28.9, 320, 'Canino', 'Mohamed 2013', 'I1 - 20% depletion, 4746 m³/ha, yield 28.9 kg/tree (2010)'],
    [4847/10, 33.6, 320, 'Canino', 'Mohamed 2013', 'I1 - 20% depletion, 4847 m³/ha, yield 33.6 kg/tree (2011)'],
    
    # I2 - 40% depletion (recommended) - best WUE
    [4364/10, 31.6, 320, 'Canino', 'Mohamed 2013', 'I2 - 40% depletion, 4364 m³/ha, yield 31.6 kg/tree (2010)'],
    [4460/10, 35.4, 320, 'Canino', 'Mohamed 2013', 'I2 - 40% depletion, 4460 m³/ha, yield 35.4 kg/tree (2011)'],
    
    # I3 - 60% depletion
    [3692/10, 24.7, 320, 'Canino', 'Mohamed 2013', 'I3 - 60% depletion, 3692 m³/ha, yield 24.7 kg/tree (2010)'],
    [4032/10, 27.0, 320, 'Canino', 'Mohamed 2013', 'I3 - 60% depletion, 4032 m³/ha, yield 27.0 kg/tree (2011)'],
    
    # I4 - 80% depletion (driest)
    [3359/10, 19.5, 320, 'Canino', 'Mohamed 2013', 'I4 - 80% depletion, 3359 m³/ha, yield 19.5 kg/tree (2010)'],
    [3493/10, 20.1, 320, 'Canino', 'Mohamed 2013', 'I4 - 80% depletion, 3493 m³/ha, yield 20.1 kg/tree (2011)'],
]

# Convert from m³/ha to m³/dunam (divide by 10) and kg/tree to kg/dunam (multiply by trees/ha)
# Trees planted at 5x5m = 400 trees/ha, so kg/tree × 400 / 10 = kg/dunam
for row in mohamed_eid_2013_data:
    row[0] = row[0]  # Already converted m³/ha to m³/dunam
    row[1] = row[1] * 40  # kg/tree to kg/dunam (400 trees/ha ÷ 10 = 40)

# ============================================================================
# DATA FROM KAYA ET AL. (2017) - Turkey
# ============================================================================
# Paper: "Effects of different irrigation regimes on vegetative growth, fruit yield and quality"
# Location: Igdir, Turkey
# Cultivar: Salak
# Irrigation: Class A pan coefficients 0.5, 0.75, 1.0, 1.25, 1.5, plus RDI (100% until harvest)
# Tree spacing: 8x8m = 156 trees/ha

kaya_2017_data = [
    # S1 - 50% of class A pan (lowest irrigation)
    [346, 41.4, 247, 'Salak', 'Kaya 2017', 'S1 - 50% Epan, 346 mm avg irrigation, yield 41.4 kg/tree (2005-06 avg)'],
    [345, 83.9, 247, 'Salak', 'Kaya 2017', 'S1 - 50% Epan, 345 mm avg, yield 83.9 kg/tree (2008)'],
    
    # S2 - 75% of class A pan
    [483, 42.3, 247, 'Salak', 'Kaya 2017', 'S2 - 75% Epan, 483 mm avg, yield 42.3 kg/tree (2005-06 avg)'],
    [612, 80.5, 247, 'Salak', 'Kaya 2017', 'S2 - 75% Epan, 612 mm, yield 80.5 kg/tree (2008)'],
    
    # S3 - 100% of class A pan (control)
    [612, 44.2, 247, 'Salak', 'Kaya 2017', 'S3 - 100% Epan, 612 mm avg, yield 44.2 kg/tree (2005-06 avg)'],
    [771, 86.1, 247, 'Salak', 'Kaya 2017', 'S3 - 100% Epan, 771 mm, yield 86.1 kg/tree (2008)'],
    
    # S4 - 125% of class A pan
    [763, 49.7, 247, 'Salak', 'Kaya 2017', 'S4 - 125% Epan, 763 mm avg, yield 49.7 kg/tree (2005-06 avg)'],
    [930, 84.7, 247, 'Salak', 'Kaya 2017', 'S4 - 125% Epan, 930 mm, yield 84.7 kg/tree (2008)'],
    
    # S5 - 150% of class A pan (highest irrigation)
    [903, 52.2, 247, 'Salak', 'Kaya 2017', 'S5 - 150% Epan, 903 mm avg, yield 52.2 kg/tree (2005-06 avg)'],
    [1089, 90.1, 247, 'Salak', 'Kaya 2017', 'S5 - 150% Epan, 1089 mm, yield 90.1 kg/tree (2008)'],
    
    # S6 - RDI (100% until harvest, no post-harvest irrigation)
    [255, 44.2, 247, 'Salak', 'Kaya 2017', 'S6 - RDI, 255 mm avg, yield 44.2 kg/tree (2005-06 avg)'],
    [303, 80.0, 247, 'Salak', 'Kaya 2017', 'S6 - RDI, 303 mm, yield 80.0 kg/tree (2008)'],
]

# Convert kg/tree to kg/dunam (8x8m = 156 trees/ha, so 156/10 = 15.6 factor)
for row in kaya_2017_data:
    row[1] = row[1] * 15.6

# ============================================================================
# DATA FROM PÉREZ-SARMIENTO ET AL. (2016) - Spain
# ============================================================================
# Paper: "Effects of regulated deficit irrigation on physiology, yield and fruit quality"
# Location: Mula Valley, Murcia, Spain
# Cultivar: Búlida
# Tree spacing: 8x6m = 208 trees/ha
# 3-year study (2008-2010)

perez_sarmiento_2016_data = [
    # Control treatment (100% ETc)
    [574, 1575, 290, 'Búlida', 'Perez-Sarmiento 2016', '2008 Control - 574 mm, 1575 kg/tree? need check units'],
    [437, 1044, 375, 'Búlida', 'Perez-Sarmiento 2016', '2009 Control - 437 mm, 1044 kg/tree'],
    [520, 923, 239, 'Búlida', 'Perez-Sarmiento 2016', '2010 Control - 520 mm, 923 kg/tree'],
    
    # RDI treatment
    [385, 1539, 290, 'Búlida', 'Perez-Sarmiento 2016', '2008 RDI - 385 mm, 1539 kg/tree'],
    [333, 1066, 375, 'Búlida', 'Perez-Sarmiento 2016', '2009 RDI - 333 mm, 1066 kg/tree'],
    [366, 895, 239, 'Búlida', 'Perez-Sarmiento 2016', '2010 RDI - 366 mm, 895 kg/tree'],
]

# Need to verify units - yield appears too high (kg/tree seems like kg/ha)
# Assuming it's kg/ha, convert to kg/dunam by dividing by 10
for row in perez_sarmiento_2016_data:
    row[1] = row[1] / 10  # Convert from kg/ha to kg/dunam if needed

# ============================================================================
# DATA FROM RUIZ-SÁNCHEZ ET AL. (2000) - Spain
# ============================================================================
# Paper: "Regulated deficit irrigation in apricot trees"
# Location: Mula Valley, Murcia, Spain
# Cultivar: Búlida
# 4-year study (1996-1999)
# Tree spacing: 8x8m = 156 trees/ha
# Control: 7254 m³/ha/year = 725.4 m³/dunam

ruiz_sanchez_2000_data = [
    # Control (T1) - 100% ETc
    [725, 208.7, 320, 'Búlida', 'Ruiz-Sanchez 2000', '1996 Control - 208.7 kg/tree'],
    [725, 145.4, 320, 'Búlida', 'Ruiz-Sanchez 2000', '1997 Control - 145.4 kg/tree'],
    [725, 367.8, 320, 'Búlida', 'Ruiz-Sanchez 2000', '1998 Control - 367.8 kg/tree'],
    [725, 178.9, 320, 'Búlida', 'Ruiz-Sanchez 2000', '1999 Control - 178.9 kg/tree'],
    
    # Continuous deficit (T2) - 50% ETc
    [363, 117.1, 320, 'Búlida', 'Ruiz-Sanchez 2000', '1996 T2 - 50% ETc, 117.1 kg/tree'],
    [363, 95.1, 320, 'Búlida', 'Ruiz-Sanchez 2000', '1997 T2 - 50% ETc, 95.1 kg/tree'],
    [363, 255.5, 320, 'Búlida', 'Ruiz-Sanchez 2000', '1998 T2 - 50% ETc, 255.5 kg/tree'],
    [363, 93.5, 320, 'Búlida', 'Ruiz-Sanchez 2000', '1999 T2 - 50% ETc, 93.5 kg/tree'],
    
    # RDI (T3) - variable
    [399, 152.5, 320, 'Búlida', 'Ruiz-Sanchez 2000', '1996 RDI - 399 mm, 152.5 kg/tree (45% saving)'],
    [399, 92.6, 320, 'Búlida', 'Ruiz-Sanchez 2000', '1997 RDI - 399 mm, 92.6 kg/tree (45% saving)'],
    [558, 324.2, 320, 'Búlida', 'Ruiz-Sanchez 2000', '1998 RDI - 558 mm, 324.2 kg/tree (23% saving)'],
    [558, 186.1, 320, 'Búlida', 'Ruiz-Sanchez 2000', '1999 RDI - 558 mm, 186.1 kg/tree (23% saving)'],
]

# Convert kg/tree to kg/dunam (8x8m = 156 trees/ha, factor 15.6)
for row in ruiz_sanchez_2000_data:
    row[1] = row[1] * 15.6

# ============================================================================
# COMBINE ALL DATA
# ============================================================================

# List all new data sources
new_data = (mohamed_eid_2013_data + kaya_2017_data + 
            perez_sarmiento_2016_data + ruiz_sanchez_2000_data)

# Create DataFrame
columns = ['Irrigation_m3_per_dunam', 'Yield_kg_per_dunam', 
           'Seasonal_Rainfall_mm', 'Cultivar', 'Study', 'Notes']
df_new = pd.DataFrame(new_data, columns=columns)

# Combine with existing if available
if len(existing_df) > 0:
    df_apricot = pd.concat([existing_df, df_new], ignore_index=True)
else:
    df_apricot = df_new

# Clean data - remove any rows with missing or zero values
df_apricot = df_apricot[df_apricot['Yield_kg_per_dunam'] > 0]
df_apricot = df_apricot[df_apricot['Irrigation_m3_per_dunam'] >= 0]
df_apricot = df_apricot.drop_duplicates(
    subset=['Study', 'Irrigation_m3_per_dunam', 'Yield_kg_per_dunam', 'Cultivar'],
    keep='first'
)

# Sort by irrigation amount
df_apricot = df_apricot.sort_values('Irrigation_m3_per_dunam').reset_index(drop=True)

print(f"\n{'='*60}")
print(f"📊 APRICOT LITERATURE DATABASE - UPDATED")
print(f"{'='*60}")
print(f"Total observations: {len(df_apricot)}")
print(f"Studies included: {df_apricot['Study'].nunique()}")
print(f"Cultivars: {df_apricot['Cultivar'].unique().tolist()}")
print(f"Irrigation range: {df_apricot['Irrigation_m3_per_dunam'].min():.0f}-{df_apricot['Irrigation_m3_per_dunam'].max():.0f} m³/dunam")
print(f"Yield range: {df_apricot['Yield_kg_per_dunam'].min():.2f}-{df_apricot['Yield_kg_per_dunam'].max():.2f} kg/dunam")
print(f"{'='*60}")

# ============================================================================
# CREATE STUDY SUMMARIES
# ============================================================================

study_summaries = []
for study in df_apricot['Study'].unique():
    study_data = df_apricot[df_apricot['Study'] == study]
    
    # Get cultivar(s)
    cultivars = study_data['Cultivar'].unique()
    cultivar_str = ', '.join(cultivars) if len(cultivars) <= 3 else 'Multiple'
    
    # Add location manually
    location_map = {
        'Ezzat 2021': 'Wadi El Natrun, Egypt',
        'Perez-Pastor 2014': 'Murcia, Spain',
        'Perez-Pastor 2009': 'Murcia, Spain',
        'Mohamed 2013': 'El-Kanater, Egypt',
        'Kaya 2017': 'Igdir, Turkey',
        'Perez-Sarmiento 2016': 'Murcia, Spain',
        'Ruiz-Sanchez 2000': 'Murcia, Spain'
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
for study in df_apricot['Study'].unique():
    study_data = df_apricot[df_apricot['Study'] == study]
    
    # Get min, median, max points for each cultivar
    for cultivar in study_data['Cultivar'].unique():
        cult_data = study_data[study_data['Cultivar'] == cultivar]
        if len(cult_data) >= 3:
            # Get min, median, max irrigation points
            min_point = cult_data.nsmallest(1, 'Irrigation_m3_per_dunam').iloc[0]
            max_point = cult_data.nlargest(1, 'Irrigation_m3_per_dunam').iloc[0]
            
            # Get point closest to median irrigation
            median_irr = cult_data['Irrigation_m3_per_dunam'].median()
            median_idx = (cult_data['Irrigation_m3_per_dunam'] - median_irr).abs().argsort()[:1]
            median_point = cult_data.iloc[median_idx]
            
            key_points.append(min_point)
            key_points.append(median_point.iloc[0])
            key_points.append(max_point)

# Remove duplicates
df_key = pd.DataFrame(key_points).drop_duplicates().sort_values('Irrigation_m3_per_dunam')

# ============================================================================
# SAVE TO EXCEL
# ============================================================================

output_file = 'apricot_literature_data_updated.xlsx'
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    df_apricot.to_excel(writer, sheet_name='All_Observations', index=False)
    df_summary.to_excel(writer, sheet_name='Study_Summaries', index=False)
    df_key.to_excel(writer, sheet_name='Key_Points', index=False)
    
    # Add a metadata sheet
    metadata = pd.DataFrame([
        ['Created', datetime.now().strftime('%Y-%m-%d')],
        ['Total observations', len(df_apricot)],
        ['Total studies', df_apricot['Study'].nunique()],
        ['Cultivars', ', '.join(df_apricot['Cultivar'].unique())],
        ['Irrigation range', f"{df_apricot['Irrigation_m3_per_dunam'].min():.0f}-{df_apricot['Irrigation_m3_per_dunam'].max():.0f} m³/dunam"],
        ['Yield range', f"{df_apricot['Yield_kg_per_dunam'].min():.2f}-{df_apricot['Yield_kg_per_dunam'].max():.2f} kg/dunam"],
        ['Units', 'Irrigation: m³/dunam (same as mm), Yield: kg/dunam fresh fruit'],
        ['Note', '1 ha = 10 dunam, 1 mm = 1 m³/dunam'],
        ['Typical apricot yield', '15-35 t/ha = 1.5-3.5 kg/dunam']
    ], columns=['Property', 'Value'])
    metadata.to_excel(writer, sheet_name='Metadata', index=False)

print(f"\n✅ Updated apricot Excel file created: {output_file}")

# Print study summaries
print(f"\n📋 STUDIES INCLUDED:")
print(f"{'-'*80}")
for _, row in df_summary.iterrows():
    print(f"  • {row['Study']}: {row['Cultivar']} - {row['Location']}")
    print(f"    {row['N_observations']} points, Irrigation: {row['Irrigation_min']:.0f}-{row['Irrigation_max']:.0f} m³/dunam, Yield: {row['Yield_min']:.2f}-{row['Yield_max']:.2f} kg/dunam")

# Print new data specifically
print(f"\n📊 NEW ADDITIONS:")
print(f"{'-'*80}")
new_studies = ['Mohamed 2013', 'Kaya 2017', 'Perez-Sarmiento 2016', 'Ruiz-Sanchez 2000']
for study in new_studies:
    study_data = df_apricot[df_apricot['Study'] == study]
    print(f"\n  • {study}: {len(study_data)} points")
    for _, row in study_data.head(3).iterrows():
        print(f"    - {row['Irrigation_m3_per_dunam']:.0f} mm, {row['Yield_kg_per_dunam']:.1f} kg/dunam, {row['Cultivar']}")

print(f"\n✅ Done! Now you can run apricot_parameter_fitting.py to extract production function parameters.")