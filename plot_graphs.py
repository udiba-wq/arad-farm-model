"""
plot_graphs.py
Creates all visualizations comparing model results with observed data
INPUT: Results from run_model.py
OUTPUT: Pop-up graphs and saved PNG files showing ALL 7 outputs as comparisons
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
import sys

# Consistent styling for all graphs
CROP_NAMES = {
    'almond': 'Almond',
    'vineyard': 'Vineyard', 
    'apricot': 'Apricot'
}

COLORS = {
    'almond': ('darkblue', 'lightblue'),
    'vineyard': ('darkgreen', 'lightgreen'),
    'apricot': ('darkorange', 'gold')  
}

def setup_graph_style(ax, title, ylabel, xlabel=None):
    """Apply consistent styling to all graphs"""
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=11)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='red', linestyle=':', linewidth=1, alpha=0.5)
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

def debug_observed_data(results):
    """Helper function to debug observed data structure"""
    first_year = sorted(results.keys())[0]
    print("\n🔍 DEBUG: Observed data structure:")
    print(f"   observed keys: {results[first_year]['observed'].keys()}")
    print(f"   actual_profits: {results[first_year]['observed'].get('actual_profits', {})}")
    print(f"   crop_area: {results[first_year]['observed'].get('crop_area', {})}")

def get_observed_profit_for_crop(results, year, crop):
    """Safely get observed profit for a crop, returns None if not available"""
    try:
        if crop in results[year]['observed']['actual_profits']:
            return results[year]['observed']['actual_profits'][crop]
    except (KeyError, AttributeError):
        pass
    return None

def get_observed_area_for_crop(results, year, crop):
    """Safely get observed area for a crop, returns None if not available"""
    try:
        if crop in results[year]['observed']['crop_area']:
            return results[year]['observed']['crop_area'][crop]
    except (KeyError, AttributeError):
        pass
    return None

def create_output1_crop_income_per_dunum(results, save_path="output1_crop_income_per_dunum.png"):
    """
    Output 1: Crop Income Per Dunam
    Shows model vs observed income per dunam for each crop
    """
    print("\n>> Generating Output 1: Crop Income Per Dunam...")
    
    years = sorted(results.keys())
    fig, axes = plt.subplots(3, 1, figsize=(12, 14))
    fig.suptitle('Output 1: Crop Income Per Dunam - Model vs Observed (2015-2025)', 
                 fontsize=16, y=0.995)
    
    for idx, (crop_key, crop_name) in enumerate(CROP_NAMES.items()):
        ax = axes[idx]
        
        model_values = []
        observed_values = []
        valid_years = []
        
        for year in years:
            if crop_key in results[year]['farm_profitability']:
                # Model income per dunam
                crop_data = results[year]['farm_profitability'][crop_key]
                model_income_per_dunam = crop_data['income_per_dunam']
                model_values.append(model_income_per_dunam)
                
               # Observed income per dunam = observed yield × price
                obs_yield = results[year]['observed']['crop_yield_dun'].get(crop_key)
                obs_price = results[year]['observed']['crop_price'].get(crop_key)
                
                if obs_yield is not None and obs_price is not None:
                    observed_income_per_dunam = obs_yield * obs_price
                    observed_values.append(observed_income_per_dunam)
                else:
                    observed_values.append(None)
                
                valid_years.append(year)
        
        if valid_years:
            # Plot model line (always available)
            ax.plot(valid_years, model_values, marker='o', 
                   label=f'{crop_name} - Model', color=COLORS[crop_key][0], 
                   linewidth=2.5, markersize=8)
            
            # Plot observed line (may have gaps)
            if any(v is not None for v in observed_values):
                ax.plot(valid_years, observed_values, marker='s', 
                       label=f'{crop_name} - Observed', color=COLORS[crop_key][1], 
                       linewidth=2.5, linestyle='--', markersize=8)
            
            setup_graph_style(ax, crop_name, 'Income per Dunam (NIS)',
                             'Year' if idx == 2 else None)
            ax.legend(loc='best', fontsize=10)
        else:
            ax.text(0.5, 0.5, f'No data for {crop_name}', 
                   ha='center', va='center', transform=ax.transAxes)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.show()
    print(f"   ✓ Saved to: {os.path.abspath(save_path)}")

def create_output2_farm_income(results, save_path="output2_farm_income.png"):
    """
    Output 2: Total Farm Income
    Shows model vs observed total farm income
    """
    print("\n>> Generating Output 2: Total Farm Income...")
    
    years = sorted(results.keys())
    model_income = [results[y]['farm_income'] for y in years]
    
    # Calculate observed farm income (sum of all crop profits)
    observed_income = []
    for year in years:
        total = 0
        for crop in CROP_NAMES.keys():
            profit = get_observed_profit_for_crop(results, year, crop)
            if profit is not None:
                total += profit
        observed_income.append(total if total > 0 else None)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    ax.plot(years, model_income, marker='o', color='blue', linewidth=2.5, 
            markersize=8, label='Model Farm Income')
    
    # Only plot observed if we have data
    if any(v is not None for v in observed_income):
        ax.plot(years, observed_income, marker='s', color='green', linewidth=2.5, 
                linestyle='--', markersize=8, label='Observed Farm Income')
    
    ax.set_title('Output 2: Total Farm Income - Model vs Observed (2015-2025)', 
                 fontsize=15, fontweight='bold')
    ax.set_ylabel('Income (NIS)', fontsize=13)
    ax.set_xlabel('Year', fontsize=13)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.5)
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.show()
    print(f"   ✓ Saved to: {os.path.abspath(save_path)}")

def create_output3_freshwater_amount(results, save_path="output3_freshwater.png"):
    """
    Output 3: Freshwater Amount
    Shows freshwater used each year (model only - observed freshwater not typically recorded)
    """
    print("\n>> Generating Output 3: Freshwater Amount...")
    
    years = sorted(results.keys())
    freshwater = [results[y]['freshwater'] for y in years]
    total_water = [results[y]['total_irrigation'] for y in years]
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Stacked bar chart showing recycled vs freshwater
    recycled = [total_water[i] - freshwater[i] for i in range(len(years))]
    
    ax.bar(years, recycled, label='Recycled Water', color='lightgreen', alpha=0.8)
    ax.bar(years, freshwater, bottom=recycled, label='Freshwater', color='lightblue', alpha=0.8)
    
    ax.set_title('Output 3: Freshwater Amount (with Recycled for context) (2015-2025)', 
                 fontsize=15, fontweight='bold')
    ax.set_ylabel('Water Volume (m³)', fontsize=13)
    ax.set_xlabel('Year', fontsize=13)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    
    # Add quota line if available and constant
    try:
        quota = results[years[0]]['recycled_quota']
        ax.axhline(y=quota, color='red', linestyle=':', linewidth=2, 
                   label=f'Recycled Quota ({quota:,.0f} m³)')
        ax.legend(fontsize=11)
    except:
        pass
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.show()
    print(f"   ✓ Saved to: {os.path.abspath(save_path)}")

def create_output4_farm_total_water(results, save_path="output4_total_water.png"):
    """
    Output 4: Farm Total Water Amount
    Shows total water use over time
    """
    print("\n>> Generating Output 4: Farm Total Water Amount...")
    
    years = sorted(results.keys())
    total_water = [results[y]['total_irrigation'] for y in years]
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    ax.plot(years, total_water, marker='o', color='steelblue', linewidth=2.5, markersize=8)
    ax.fill_between(years, total_water, alpha=0.3, color='steelblue')
    
    ax.set_title('Output 4: Farm Total Water Consumption (2015-2025)', 
                 fontsize=15, fontweight='bold')
    ax.set_ylabel('Total Water (m³)', fontsize=13)
    ax.set_xlabel('Year', fontsize=13)
    ax.grid(True, alpha=0.5)
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.show()
    print(f"   ✓ Saved to: {os.path.abspath(save_path)}")

def create_output5_farm_water_price(results, save_path="output5_farm_water_price.png"):
    """
    Output 5: Farm Water Price (same for all crops)
    Shows average water price over time
    """
    print("\n>> Generating Output 5: Farm Water Price...")
    
    years = sorted(results.keys())
    avg_price = [results[y]['farm_water_price'] for y in years]
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    ax.plot(years, avg_price, marker='o', color='purple', linewidth=2.5, markersize=8)
    ax.fill_between(years, avg_price, alpha=0.3, color='purple')
    
    ax.set_title('Output 5: Farm Average Water Price (2015-2025)', 
                 fontsize=15, fontweight='bold')
    ax.set_ylabel('Average Water Price (NIS/m³)', fontsize=13)
    ax.set_xlabel('Year', fontsize=13)
    ax.grid(True, alpha=0.5)
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.2f}'))
    
    # Add horizontal line for fresh and recycled prices for reference
    try:
        fresh_price = results[years[0]]['fresh_price']
        recycled_price = results[years[0]]['recycled_price']
        ax.axhline(y=fresh_price, color='red', linestyle=':', alpha=0.5, 
                   label=f'Freshwater Price ({fresh_price} NIS/m³)')
        ax.axhline(y=recycled_price, color='green', linestyle=':', alpha=0.5, 
                   label=f'Recycled Price ({recycled_price} NIS/m³)')
        ax.legend(fontsize=10)
    except:
        pass
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.show()
    print(f"   ✓ Saved to: {os.path.abspath(save_path)}")

def create_output6_farm_water_costs(results, save_path="output6_farm_water_costs.png"):
    """
    Output 6: Farm Water Costs
    Shows total farm water costs over time
    """
    print("\n>> Generating Output 6: Farm Water Costs...")
    
    years = sorted(results.keys())
    water_costs = [results[y]['water_price_total'] for y in years]
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    ax.plot(years, water_costs, marker='o', color='coral', linewidth=2.5, markersize=8)
    ax.fill_between(years, water_costs, alpha=0.3, color='coral')
    
    ax.set_title('Output 6: Farm Total Water Costs (2015-2025)', 
                 fontsize=15, fontweight='bold')
    ax.set_ylabel('Total Water Cost (NIS)', fontsize=13)
    ax.set_xlabel('Year', fontsize=13)
    ax.grid(True, alpha=0.5)
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.show()
    print(f"   ✓ Saved to: {os.path.abspath(save_path)}")

def create_output7_farm_total_profit(results, save_path="output7_farm_profit.png"):
    """
    Output 7: Farm Total Profit
    Shows model vs observed farm profit
    """
    print("\n>> Generating Output 7: Farm Total Profit...")
    
    years = sorted(results.keys())
    model_profit = [results[y]['farm_total_profit'] for y in years]
    
    # Calculate observed profit
    observed_profit = []
    for year in years:
        # Sum all observed crop profits
        total_observed = 0
        for crop in CROP_NAMES.keys():
            profit = get_observed_profit_for_crop(results, year, crop)
            if profit is not None:
                total_observed += profit
        
        if total_observed > 0:
            # Observed profit = observed income - model costs
            # (We assume costs are the same, difference comes from revenue)
            model_costs = results[year]['total_costs']['total']
            observed_profit.append(total_observed)
        else:
            observed_profit.append(None)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    ax.plot(years, model_profit, marker='o', color='darkblue', linewidth=2.5, 
            markersize=8, label='Model Profit')
    
    if any(v is not None for v in observed_profit):
        ax.plot(years, observed_profit, marker='s', color='darkgreen', linewidth=2.5, 
                linestyle='--', markersize=8, label='Observed Profit')
    
    # Add zero line
    ax.axhline(y=0, color='red', linestyle=':', linewidth=1.5, alpha=0.7, label='Break-even')
    
    ax.set_title('Output 7: Farm Total Profit - Model vs Observed (2015-2025)', 
                 fontsize=15, fontweight='bold')
    ax.set_ylabel('Profit (NIS)', fontsize=13)
    ax.set_xlabel('Year', fontsize=13)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.5)
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.show()
    print(f"   ✓ Saved to: {os.path.abspath(save_path)}")

def create_output8_crop_yield_comparison(results, save_path="output8_crop_yield_comparison.png"):
    """
    Output 8: Crop Yield Comparison (NEW)
    Shows model vs observed yield for each crop
    """
    print("\n>> Generating Output 8: Crop Yield Comparison...")
    
    years = sorted(results.keys())
    fig, axes = plt.subplots(3, 1, figsize=(12, 14))
    fig.suptitle('Crop Yield: Model vs Observed (2015-2025)', 
                 fontsize=16, y=0.995)
    
    for idx, (crop_key, crop_name) in enumerate(CROP_NAMES.items()):
        ax = axes[idx]
        
        model_yields = []
        observed_yields = []
        valid_years = []
        
        for year in years:
            if crop_key in results[year]['farm_profitability']:
                # Model yield from production function
                crop_data = results[year]['farm_profitability'][crop_key]
                model_yield = crop_data['yield_per_dunam']
                model_yields.append(model_yield)
                
                # Calculate observed yield from profit data
                observed_profit = get_observed_profit_for_crop(results, year, crop_key)
                observed_area = get_observed_area_for_crop(results, year, crop_key)
                crop_price = None
                
                # Get crop price from observed data or model
                if 'crop_price' in results[year]['observed']:
                    crop_price = results[year]['observed']['crop_price'].get(crop_key)
                
                # If price not in observed, try to get from model inputs
                if crop_price is None and crop_key in results[year]['farm_profitability']:
                    # Approximate price from model income and yield
                    model_income = crop_data['income_per_dunam']
                    if model_yield > 0:
                        crop_price = model_income / model_yield
                
                if (observed_profit is not None and observed_area is not None and 
                    observed_area > 0 and crop_price is not None and crop_price > 0):
                    
                    # Observed yield = observed profit / (area * price)
                    observed_yield = results[year]['observed']['crop_yield_dun'].get(crop_key)
                    observed_yields.append(observed_yield)
                else:
                    observed_yields.append(None)
                
                valid_years.append(year)
        
        if valid_years:
            # Plot model yield line
            ax.plot(valid_years, model_yields, marker='o', 
                   label=f'{crop_name} - Model', color=COLORS[crop_key][0], 
                   linewidth=2.5, markersize=8)
            
            # Plot observed yield line (may have gaps)
            if any(v is not None for v in observed_yields):
                ax.plot(valid_years, observed_yields, marker='s', 
                       label=f'{crop_name} - Observed', color=COLORS[crop_key][1], 
                       linewidth=2.5, linestyle='--', markersize=8)
            
            setup_graph_style(ax, f'{crop_name} Yield', 'Yield (kg/dunam)',
                             'Year' if idx == 2 else None)
            ax.legend(loc='best', fontsize=10)
        else:
            ax.text(0.5, 0.5, f'No yield data for {crop_name}', 
                   ha='center', va='center', transform=ax.transAxes)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.show()
    print(f"   ✓ Saved to: {os.path.abspath(save_path)}")

def create_all_graphs(results):
    """
    Generate all 8 output graphs (original 7 + new yield comparison)
    """
    print("\n" + "=" * 60)
    print("GENERATING ALL 8 OUTPUT GRAPHS")
    print("=" * 60)
    
    # Debug first to see what data we have
    debug_observed_data(results)
    
    # Original 7 outputs
    create_output1_crop_income_per_dunum(results)
    create_output2_farm_income(results)
    create_output3_freshwater_amount(results)
    create_output4_farm_total_water(results)
    create_output5_farm_water_price(results)
    create_output6_farm_water_costs(results)
    create_output7_farm_total_profit(results)
    
    # NEW: Yield comparison graphs
    create_output8_crop_yield_comparison(results)
    
    print("\n✅ All 8 output graphs generated successfully!")
if __name__ == "__main__":
    print("=" * 50)
    print("TESTING plot_graphs.py")
    print("=" * 50)
    
    # Import real data from run_model
    try:
        from run_model import run_model_for_all_years
        print("\n📊 Loading real model results...")
        results = run_model_for_all_years()
        
        # Generate all 7 graphs
        create_all_graphs(results)
        
    except ImportError as e:
        print(f"\n❌ Error: Could not import run_model.py")
        print(f"   {e}")
        print("   Please make sure run_model.py is in the same directory")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n✅ Test complete!")