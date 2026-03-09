# Arad Valley Farm Profitability Model

**A dual-source irrigation optimization model for perennial crops under differentiated water pricing**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Research: PhD](https://img.shields.io/badge/Research-PhD-purple.svg)]()

## 📋 Overview

This model simulates and optimizes farm profitability for a 400-hectar perennial crop farm in the Arad Valley, Israel, operating under a dual-source irrigation system (limited recycled water quota + unlimited freshwater). The farm cultivates almonds, vineyards, and apricots.

The model integrates:
- **Crop production functions** (piecewise linear with plateau)
- **Tiered water pricing** (cheap recycled water up to quota, expensive freshwater beyond)
- **Farm-level economics** (fixed costs, variable costs, administrative expenses)
- **Validation framework** comparing model predictions with observed farm data

## 🎯 Research Objectives

1. Develop crop-specific production functions for almonds, vineyards, and apricots
2. Characterize water cost behavior under dual-source supply
3. Quantify relationships between land allocation, irrigation intensity, and profitability
4. Determine profit-maximizing resource allocation through optimization

## 🏗️ Project Structure

```
├── 📄 observed_data.py          # Loads and organizes observed farm data from Excel
├── 📄 calculation_functions.py  # Core model classes with 14 production functions
├── 📄 run_model.py               # Applies calculations to observed data for all years
├── 📄 plot_graphs.py             # Generates all 7 output graphs with comparisons
├── 📄 derive_parameters.py       # Derives A, B, threshold parameters from literature
├── 📄 requirements.txt           # Python package dependencies
├── 📄 README.md                   # This file
├── 📁 data/                       # Excel data files (not in repo)
│   ├── 📊 Model_inp_1_26.xlsx    # Input data (crops, water, expenses)
│   └── 📊 Tot_farm_prof.xlsx      # Observed profits for validation
└── 📁 output/                      # Generated outputs
    ├── 📊 farm_profit.png
    ├── 📊 crop_yields.png
    └── ...
```

## 🧮 The 14 Core Functions

| Function | Description | Implementation |
|----------|-------------|----------------|
| F1 | Production Function | `Crop.production_function()` |
| F2 | Income Per Dunam | `Crop.income_per_dunam_function()` |
| F3 | Income Area Function | `Farm.income_area_function()` |
| F4 | Farm Income Function | `Farm.farm_income_function()` |
| F5 | Irrigation Area Function | `Farm.irrigation_area_function()` |
| F6 | Total Irrigation Function | `Farm.total_irrigation_function()` |
| F7 | Freshwater Function | `Farm.freshwater_function()` |
| F8 | Water Price Function | `Farm.water_price_function()` |
| F9 | Farm Water Price | `Farm.farm_water_price_function()` |
| F10 | Crop Water Cost Per Dunam | `Crop.water_cost_per_dunam_function()` |
| F11 | Fixed Costs Function | `Crop.fixed_costs_per_dunam_function()` |
| F12 | Farm Fixed Costs | `Farm.farm_fixed_costs_function()` |
| F13 | Total Costs Function | `Farm.total_costs_function()` |
| F14 | Farm Profitability | `Farm.farm_profitability_function()` |

## 📊 The 7 Outputs

| Output | Description | Graph |
|--------|-------------|-------|
| O1 | Crop Income Per Dunam | `output1_crop_income_per_dunum.png` |
| O2 | Total Farm Income | `output2_farm_income.png` |
| O3 | Freshwater Amount | `output3_freshwater.png` |
| O4 | Farm Total Water Amount | `output4_total_water.png` |
| O5 | Farm Water Price | `output5_farm_water_price.png` |
| O6 | Farm Water Costs | `output6_farm_water_costs.png` |
| O7 | Farm Total Profit | `output7_farm_profit.png` |

## 🚀 Getting Started

### Prerequisites
```bash
python -m pip install pandas numpy matplotlib openpyxl scipy
```

### Quick Start
```bash
# 1. Test data loading
python observed_data.py

# 2. Test calculation functions
python calculation_functions.py

# 3. Run full model for all years
python run_model.py

# 4. Generate all graphs
python plot_graphs.py

# 5. Derive production parameters from literature
python derive_parameters.py
```

## 📁 Data Requirements

### `Model_inp_1_26.xlsx` - Three sheets:
- **Crop_Data**: Yearly crop parameters (A, B, thresholds, areas, prices, irrigation)
- **Farm_Details**: Water parameters (recycled quota, fresh price, recycled price)
- **Expenses**: Administrative costs

### `Tot_farm_prof.xlsx` - Observed profits:
- Year, crop type, total crop profit, area, irrigation, costs

## 🔧 Key Parameters

| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| A | Production function slope | 0.10-0.25 kg/m³ |
| B | Intercept (zero irrigation yield) | 30-60 kg/dunam |
| θ | Irrigation threshold | 800-1250 m³/dunam |
| Fresh price | Freshwater cost | ~2.5 NIS/m³ |
| Recycled price | Recycled water cost | ~0.5 NIS/m³ |
| Quota | Annual recycled water allocation | ~1.5 million m³ |

## 📈 Sample Output

```
Year   | Model Profit | Actual Profit | Yields (A/V/Ap)
---------------------------------------------------------
2015.0 |   1,510,500 |     -131,960 | 206.0 / 180.5 / 195.2
2016.0 |   1,856,696 |     -354,336 | 227.0 / 195.3 / 208.7
...
2025.0 |   5,733,706 |    2,825,122 | 332.0 / 285.6 / 301.4
```

## 📚 Literature Sources for Production Functions

The model's production functions are informed by:
- **Goldhamer & Fereres (2017)** - California almond trials
- **Mirás-Avalos et al. (2023)** - Spanish meta-analysis
- **Egea et al. (2010)** - PRD strategies in almond
- **López-López et al. (2018)** - RDI vs SDI comparison
- **Girona et al. (2005)** - RDI during kernel filling

## 🤝 Contributing

This is a PhD research project supervised by Prof. Tal Svoray and Dr. Tamir Kamai at Ben-Gurion University of the Negev and the Volcani Institute.

For questions or collaboration:
- 📧 Udi Ben Ari: [your-email]
- 🏫 Ben-Gurion University, Department of Geography and Environmental Development
- 🌾 Volcani Institute, Department of Soil Chemistry, Plant Nutrition and Microbiology

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Prof. Tal Svoray for supervision and guidance
- Dr. Tamir Kamai for model development support
- The Arad Valley Agricultural Farm for providing data
- Israeli Water Authority for water pricing information

## 📝 Citation

If you use this model in your research, please cite:

```
Ben Ari, U., Svoray, T., & Kamai, T. (2026). 
Arad Valley Farm Profitability Model: 
Optimizing irrigation under dual-source water pricing. 
[Software]. GitHub. https://github.com/[username]/arad-farm-model
```