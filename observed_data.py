"""
observed_data.py
Load observed farm data from Excel files.

Source-of-truth rules:
    model_parameters.xlsx  -> Production_Functions sheet: A, B, thresholds only
    farm_data.xlsx         -> Crop_Data:  crop_area, irrigation, price,
                                          fixed_exp, est_costs, Yield_dun, tot_crop_prof
                           -> Water_Data: recycled_quota, fresh_price, recycled_price
                           -> Admin_Data: general_admin_costs
"""

import pandas as pd
import sys

MODEL_PARAMS_FILE = r"C:\Users\אודי בן ארי\Documents\מאמרים לסקירת ספרות\data\2026_3_9_model_parameters.xlsx"
FARM_DATA_FILE    = r"C:\Users\אודי בן ארי\Documents\מאמרים לסקירת ספרות\data\2026_3_9_farm_data.xlsx"

def validate_crop_uniqueness(df, label):
    """Ensure each crop appears only once per year."""
    dupes = df.groupby(['year', 'c_type']).size().reset_index(name='count')
    dupes = dupes[dupes['count'] > 1]
    if not dupes.empty:
        print(f"ERROR: Duplicate crop entries in {label}!")
        for _, row in dupes.iterrows():
            print(f"  Year {row['year']}, Crop {row['c_type']}: {row['count']} entries")
        sys.exit(1)
    print(f"Validation passed: {label}")


def load_all_years_data():
    """
    Load and return all yearly data organised by year.

    Flow:
        df_prod_functions  -> crop_A, crop_B, crop_thresholds   (model parameters)
        df_crop_data       -> crop_area, crop_irrigation,
                              crop_price, crop_fixed_exp,
                              crop_est_costs, crop_yield_dun,
                              actual_profits                     (observed farm data)
        df_water_data      -> recycled_quota, fresh_price,
                              recycled_price                     (farm water parameters)
        df_admin_data      -> admin_cost                         (farm admin costs)
    """
    print("Loading data from Excel files...")

    try:
        df_prod_functions = pd.read_excel(MODEL_PARAMS_FILE, sheet_name='Production_Functions', engine='openpyxl')
        df_crop_data      = pd.read_excel(FARM_DATA_FILE,    sheet_name='Crop_Data',            engine='openpyxl')
        df_water_data     = pd.read_excel(FARM_DATA_FILE,    sheet_name='Water_Data',           engine='openpyxl')
        df_admin_data     = pd.read_excel(FARM_DATA_FILE,    sheet_name='Admin_Data',           engine='openpyxl')
        
        # Standardise column names to match code expectations
        df_prod_functions = df_prod_functions.rename(columns={
    'Year': 'year',
    'Crop Type': 'c_type',
    'A\n(slope, kg/m³)':        'A',
    'B\n(intercept, kg/dunam)': 'B',
    'Threshold\n(m³/dunam)':    'threshold',
})

        df_crop_data = df_crop_data.rename(columns={})

        df_water_data = df_water_data.rename(columns={
    'Year': 'year',
    'Recycled Quota\n(m³)':      'recycled_quota',
    'Fresh Price\n(NIS/m³)':     'fresh_price',
    'Recycled Price\n(NIS/m³)':  'recycled_price',
    })

        df_admin_data = df_admin_data.rename(columns={
    'Year': 'year',
    'General Admin\nCosts (NIS)': 'admin_cost',
})
        print("All files loaded successfully")
    except Exception as e:
        print(f"Error loading files: {e}")
        sys.exit(1)

    # ── Clean production functions ─────────────────────────────────────────────
    df_prod_functions['c_type'] = df_prod_functions['c_type'].astype(str).str.lower().str.strip()
    df_prod_functions = df_prod_functions.dropna(subset=['year', 'c_type'])
    df_prod_functions['year'] = df_prod_functions['year'].astype(int)
    validate_crop_uniqueness(df_prod_functions, 'Production_Functions')

    # ── Clean crop data ────────────────────────────────────────────────────────
    df_crop_data['c_type'] = df_crop_data['c_type'].astype(str).str.lower().str.strip()
    df_crop_data = df_crop_data.dropna(subset=['year', 'c_type'])
    df_crop_data['year'] = df_crop_data['year'].astype(int)
    validate_crop_uniqueness(df_crop_data, 'Crop_Data')

    # ── Clean water data ───────────────────────────────────────────────────────
    df_water_data = df_water_data.dropna(subset=['year'])
    df_water_data['year'] = df_water_data['year'].astype(int)

    # ── Clean admin data ───────────────────────────────────────────────────────
    df_admin_data = df_admin_data.dropna(subset=['year'])
    df_admin_data['year'] = df_admin_data['year'].astype(int)

    # ── Build water dict keyed by year ─────────────────────────────────────────
    # Each row in Water_Data is one year with three columns

    water_dict = {}
    for _, row in df_water_data.iterrows():
        year = int(row['year'])
        water_dict[year] = {
            'recycled_quota':  row['recycled_quota'],
            'fresh_price':     row['fresh_price'],
            'recycled_price':  row['recycled_price'],
        }

    # ── Build admin dict keyed by year ─────────────────────────────────────────
    admin_dict = {}
    for _, row in df_admin_data.iterrows():
        year = int(row['year'])
        admin_dict[year] = row['admin_cost']

    # ── Build crop data dict keyed by (year, crop) ─────────────────────────────
    # Source of truth for all observed field data
    crop_data_dict = {}
    for _, row in df_crop_data.iterrows():
        year = int(row['year'])
        crop = row['c_type']
        crop_data_dict.setdefault(year, {})[crop] = {
            'crop_area':       row['crop_area'],
            'crop_irrigation': row['crop_irrigation'],
            'crop_price':      row['crop_price'],
            'fixed_exp':       row['fixed_exp'],
            'est_costs':       row['est_costs'],
            'yield_dun':       row['yield_dun'],
            'tot_crop_prof':   row['tot_crop_prof'],
    }

    # ── Build production functions dict keyed by (year, crop) ─────────────────
    # Model parameters only — A, B, thresholds
    prod_dict = {}
    for _, row in df_prod_functions.iterrows():
        year = int(row['year'])
        crop = row['c_type']
        prod_dict.setdefault(year, {})[crop] = {
           'A':         row['A'],
            'B':         row['B'],
            'threshold': row['threshold'],
        }

    # ── Assemble yearly_data ───────────────────────────────────────────────────
    years = sorted(df_prod_functions['year'].unique())
    yearly_data = {}

    for year in years:
        if year not in water_dict:
            print(f"  Warning: No water data for {year}, skipping")
            continue
        if year not in crop_data_dict:
            print(f"  Warning: No crop data for {year}, skipping")
            continue

        # Initialise per-crop dicts
        crop_A = {};         crop_B = {};          crop_thresholds = {}
        crop_area = {};      crop_irrigation = {};  crop_price = {}
        crop_fixed_exp = {}; crop_est_costs = {}
        crop_yield_dun = {}; actual_profits = {}

        for crop, params in prod_dict.get(year, {}).items():
            # Model parameters — from model_parameters.xlsx
            crop_A[crop]          = params['A']
            crop_B[crop]          = params['B']
            crop_thresholds[crop] = params['threshold']

            # Observed field data — from farm_data.xlsx Crop_Data
            if crop in crop_data_dict.get(year, {}):
                obs = crop_data_dict[year][crop]
                crop_area[crop]       = obs['crop_area']
                crop_irrigation[crop] = obs['crop_irrigation']
                crop_price[crop]      = obs['crop_price']
                crop_fixed_exp[crop]  = obs['fixed_exp']
                crop_est_costs[crop]  = obs['est_costs']
                crop_yield_dun[crop]  = obs['yield_dun']
                actual_profits[crop]  = obs['tot_crop_prof']
            else:
                print(f"  Warning: No crop data for {crop} in {year}")

        yearly_data[year] = {
            # Model parameters (model_parameters.xlsx)
            'crop_A':          crop_A,
            'crop_B':          crop_B,
            'crop_thresholds': crop_thresholds,

            # Observed crop data (farm_data.xlsx — Crop_Data)
            'crop_area':       crop_area,
            'crop_irrigation': crop_irrigation,
            'crop_price':      crop_price,
            'crop_fixed_exp':  crop_fixed_exp,
            'crop_est_costs':  crop_est_costs,
            'crop_yield_dun':  crop_yield_dun,   # direct observed yield
            'actual_profits':  actual_profits,

            # Farm water parameters (farm_data.xlsx — Water_Data)
            'recycled_quota':  water_dict[year]['recycled_quota'],
            'fresh_price':     water_dict[year]['fresh_price'],
            'recycled_price':  water_dict[year]['recycled_price'],

            # Farm admin costs (farm_data.xlsx — Admin_Data)
            'admin_cost':      admin_dict.get(year, 0),
        }

    print(f"Data loaded for years: {sorted(yearly_data.keys())}")
    return yearly_data


def print_data_summary(yearly_data):
    """Print a summary of the loaded data."""
    print("\n" + "=" * 60)
    print("DATA SUMMARY")
    print("=" * 60)
    for year, data in sorted(yearly_data.items()):
        print(f"\n📅 Year {year}:")
        print(f"   Water: quota={data['recycled_quota']:,.0f} m³  "
              f"fresh={data['fresh_price']} NIS/m³  "
              f"recycled={data['recycled_price']} NIS/m³")
        print(f"   Admin: {data['admin_cost']:,.0f} NIS")
        for crop in sorted(data['crop_yield_dun']):
            print(f"   {crop:10}: area={data['crop_area'][crop]:.0f} dun  "
                  f"irr={data['crop_irrigation'][crop]:.0f} m³/dun  "
                  f"yield={data['crop_yield_dun'][crop]:.0f} kg/dun  "
                  f"price={data['crop_price'][crop]:.2f} NIS/kg")


if __name__ == "__main__":
    print("=" * 50)
    print("TESTING observed_data.py")
    print("=" * 50)
    data = load_all_years_data()
    print_data_summary(data)
    print("\n✅ Test complete!")