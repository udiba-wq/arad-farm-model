
# apricot_parameter_fitting.py
# Fit production functions to apricot literature data

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats

# Load the data
df = pd.read_excel('apricot_literature_data.xlsx', sheet_name='All_Observations')

# Define piecewise linear function
def piecewise_linear(irrigation, A, B, threshold):
    return np.piecewise(irrigation, 
                        [irrigation <= threshold, irrigation > threshold],
                        [lambda x: A * x + B, 
                         lambda x: A * threshold + B])

print("\n📊 APRICOT PRODUCTION FUNCTION ANALYSIS")
print("="*60)

# Method 1: Fit to all data (pooled)
x_all = df['Irrigation_m3_per_dunam'].values
y_all = df['Yield_kg_per_dunam'].values
sort_idx = np.argsort(x_all)
x_all = x_all[sort_idx]
y_all = y_all[sort_idx]

# Initial guess - apricot parameters are between almond and grape
p0 = [0.03, 5, 600]
bounds = ([0, 0, 300], [0.1, 20, 1000])

try:
    popt_pooled, _ = curve_fit(piecewise_linear, x_all, y_all, p0=p0, bounds=bounds)
    A_pooled, B_pooled, threshold_pooled = popt_pooled
    y_max_pooled = A_pooled * threshold_pooled + B_pooled
    
    print("\n📊 POOLED PRODUCTION FUNCTION (ALL DATA)")
    print(f"A (slope): {A_pooled:.4f} kg/m³")
    print(f"B (intercept): {B_pooled:.2f} kg/dunam")
    print(f"Threshold: {threshold_pooled:.0f} m³/dunam")
    print(f"Maximum yield: {y_max_pooled:.2f} kg/dunam")
    
except Exception as e:
    print(f"Pooled fit failed: {e}")

# Method 2: Fit by cultivar
print("\n📊 CULTIVAR-SPECIFIC PARAMETERS")
print("="*60)
for cultivar in df['Cultivar'].unique():
    cult_data = df[df['Cultivar'] == cultivar]
    if len(cult_data) < 3:
        continue
    
    x_cult = cult_data['Irrigation_m3_per_dunam'].values
    y_cult = cult_data['Yield_kg_per_dunam'].values
    sort_idx = np.argsort(x_cult)
    x_cult = x_cult[sort_idx]
    y_cult = y_cult[sort_idx]
    
    try:
        popt, _ = curve_fit(piecewise_linear, x_cult, y_cult, p0=p0, bounds=bounds)
        A, B, thresh = popt
        print(f"\n{cultivar}:")
        print(f"  A = {A:.4f} kg/m³")
        print(f"  B = {B:.2f} kg/dunam")
        print(f"  Threshold = {thresh:.0f} m³/dunam")
        print(f"  Y_max = {A*thresh + B:.2f} kg/dunam")
        print(f"  n = {len(cult_data)}")
    except Exception as e:
        print(f"  {cultivar}: Could not fit - {e}")

# Create visualization
fig, ax = plt.subplots(figsize=(12, 8))

# Plot all data points with different colors for each study
colors = {'Ezzat 2021': 'red', 'Perez-Pastor 2014': 'blue', 'Perez-Pastor 2009': 'green'}
markers = {'Ninfa': 'o', 'Canino': 's', 'Búlida': '^'}

for _, row in df.iterrows():
    color = colors.get(row['Study'], 'gray')
    marker = markers.get(row['Cultivar'], 'o')
    ax.scatter(row['Irrigation_m3_per_dunam'], row['Yield_kg_per_dunam'], 
              color=color, marker=marker, s=50, alpha=0.7)

# Add legend elements
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='red', label='Ezzat 2021'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', label='Perez-Pastor 2014'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='green', label='Perez-Pastor 2009'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', label='Ninfa (circle)'),
    Line2D([0], [0], marker='s', color='w', markerfacecolor='gray', label='Canino (square)'),
    Line2D([0], [0], marker='^', color='w', markerfacecolor='gray', label='Búlida (triangle)')
]

# Plot pooled fit
x_smooth = np.linspace(0, 1100, 100)
y_smooth = piecewise_linear(x_smooth, A_pooled, B_pooled, threshold_pooled)
ax.plot(x_smooth, y_smooth, 'k-', linewidth=3, label='Pooled fit')
ax.axvline(x=threshold_pooled, color='gray', linestyle='--', alpha=0.7)

ax.set_xlabel('Irrigation (m³/dunam)', fontsize=12)
ax.set_ylabel('Yield (kg/dunam)', fontsize=12)
ax.set_title('Apricot Production Functions - Literature Compilation', fontsize=14)
ax.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('apricot_production_functions.png', dpi=150)
plt.show()
