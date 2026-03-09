"""
run_model.py
Applies calculation functions to observed data for all years
INPUT: Observed data from observed_data.py
OUTPUT: Dictionary of model-calculated results for all years
"""

from observed_data import load_all_years_data, print_data_summary
from calculation_functions import Crop, Farm

def create_crop_objects(year_data):
    """
    Create Crop objects for a single year from observed data
    
    Input: year_data dictionary from observed_data.py
    Output: list of Crop objects
    """
    crops = []
    
    # Get all crop types present in this year
    crop_types = list(year_data['crop_A'].keys())
    
    for crop_type in crop_types:
        # Extract parameters for this crop from observed data
        crop = Crop(
            crop_type=crop_type,
            A=year_data['crop_A'][crop_type],
            B=year_data['crop_B'][crop_type],
            fixed_exp=year_data['crop_fixed_exp'][crop_type],
            est_costs=year_data['crop_est_costs'][crop_type],
            thresholds=year_data['crop_thresholds'][crop_type]
        )
        crops.append(crop)
    
    return crops

def prepare_crop_data_for_farm(year_data):
    """
    Prepare the crop data dictionary needed by Farm class
    
    Input: year_data dictionary from observed_data.py
    Output: dictionary with 'areas', 'irrigations', 'prices'
    """
    return {
        'areas': year_data['crop_area'],
        'irrigations': year_data['crop_irrigation'],
        'prices': year_data['crop_price']
    }

def prepare_water_params(year_data):
    """
    Prepare water parameters dictionary needed by Farm class
    
    Input: year_data dictionary from observed_data.py
    Output: dictionary with water parameters
    """
    return {
        'recycled_quota': year_data['recycled_quota'],
        'fresh_price': year_data['fresh_price'],
        'recycled_price': year_data['recycled_price']
    }

def run_model_for_year(year, year_data):
    """
    Run the model for a single year
    
    Input:
        year: integer
        year_data: dictionary from observed_data.py
    
    Output: dictionary with all 14 function results for this year
    """
    print(f"  Running model for {year}...")
    
    # Create Crop objects from observed data
    crops = create_crop_objects(year_data)
    
    # Prepare data for Farm class
    crop_data = prepare_crop_data_for_farm(year_data)
    water_params = prepare_water_params(year_data)
    admin_cost = year_data['admin_cost']
    
    # Create Farm object
    farm = Farm(crops, crop_data, water_params, admin_cost)
    
    # Run all 14 functions
    results = farm.get_all_results()
    
    # Also store the observed data for later comparison
    results['observed'] = {
        'actual_profits': year_data['actual_profits'],
        'crop_area': year_data['crop_area'],
        'crop_price': year_data['crop_price'],
        'crop_irrigation': year_data['crop_irrigation'],
        'crop_yield_dun': year_data['crop_yield_dun']
    }
    
    return results

def run_model_for_all_years():
    """
    Run the model for all years in the observed data
    
    Output: dictionary {
        2015: {all 14 function results for 2015},
        2016: {all 14 function results for 2016},
        ...
    }
    """
    print("\n" + "=" * 60)
    print("RUNNING MODEL CALCULATIONS FOR ALL YEARS")
    print("=" * 60)
    
    # Load observed data
    print("\n📂 Loading observed farm data...")
    all_observed_data = load_all_years_data()
    
    # Run model for each year
    print("\n🔄 Running calculations...")
    all_model_results = {}
    
    for year, year_data in all_observed_data.items():
        results = run_model_for_year(year, year_data)
        all_model_results[year] = results
        print(f"    ✅ {year} complete")
    
    print(f"\n✅ Model run complete for years: {sorted(all_model_results.keys())}")
    return all_model_results

def print_model_results_summary(results):
    """
    Print a summary of model results for verification
    
    Input: results dictionary from run_model_for_all_years()
    """
    print("\n" + "=" * 60)
    print("MODEL RESULTS SUMMARY")
    print("=" * 60)
    
    for year, year_results in sorted(results.items()):
        print(f"\n📅 {year}:")
        print(f"   Farm Income: {year_results['farm_income']:>12,.0f} NIS")
        print(f"   Total Costs: {year_results['total_costs']['total']:>12,.0f} NIS")
        print(f"   Farm Profit: {year_results['farm_total_profit']:>12,.0f} NIS")
        print(f"   Total Water: {year_results['total_irrigation']:>12,.0f} m³")
        print(f"   Avg Water Price: {year_results['farm_water_price']:>10.2f} NIS/m³")
        
        # Show per-crop yields
        yields = year_results['production_function']
        yield_str = ", ".join([f"{c}: {y:>5.1f}" for c, y in yields.items()])
        print(f"   Yields (kg/dunam): {yield_str}")
        
        # Show per-crop profits
        profits = {c: p['profit'] for c, p in year_results['farm_profitability'].items()}
        profit_str = ", ".join([f"{c}: {p:>10,.0f}" for c, p in profits.items()])
        print(f"   Profits (NIS): {profit_str}")

def compare_with_observed(results):
    """
    Compare model results with observed data
    
    Input: results dictionary from run_model_for_all_years()
    """
    print("\n" + "=" * 60)
    print("MODEL VS OBSERVED COMPARISON")
    print("=" * 60)
    
    for year, year_results in sorted(results.items()):
        print(f"\n📅 {year}:")
        
        # Get observed profits
        observed_profits = year_results['observed']['actual_profits']
        
        # Get model profits
        model_profits = {c: p['profit'] for c, p in year_results['farm_profitability'].items()}
        
        # Compare for each crop
        all_crops = set(list(observed_profits.keys()) + list(model_profits.keys()))
        
        for crop in sorted(all_crops):
            observed = observed_profits.get(crop, 0)
            model = model_profits.get(crop, 0)
            diff = model - observed
            pct_diff = (diff / observed * 100) if observed != 0 else float('inf')
            
            print(f"   {crop:10}: Observed={observed:>10,.0f}  Model={model:>10,.0f}  "
                  f"Diff={diff:>+10,.0f}  ({pct_diff:>+5.1f}%)")

def get_results_for_graphs(results):
    """
    Prepare results in a format ready for plotting
    
    Input: results dictionary from run_model_for_all_years()
    Output: dictionary with structured data for graphs
    """
    graph_data = {
        'years': sorted(results.keys()),
        'farm_profit': {},
        'farm_income': {},
        'farm_costs': {},
        'total_water': {},
        'avg_water_price': {},
        'crop_yield': {'almond': [], 'vineyard': [], 'apricot': []},
        'crop_profit': {'almond': [], 'vineyard': [], 'apricot': []},
        'crop_profit_per_dunam': {'almond': [], 'vineyard': [], 'apricot': []},
        'observed_profit': {'almond': [], 'vineyard': [], 'apricot': []}
    }
    
    for year in sorted(results.keys()):
        year_res = results[year]
        
        # Farm-level data
        graph_data['farm_profit'][year] = year_res['farm_total_profit']
        graph_data['farm_income'][year] = year_res['farm_income']
        graph_data['farm_costs'][year] = year_res['total_costs']['total']
        graph_data['total_water'][year] = year_res['total_irrigation']
        graph_data['avg_water_price'][year] = year_res['farm_water_price']
        
        # Crop-level data
        for crop in ['almond', 'vineyard', 'apricot']:
            if crop in year_res['farm_profitability']:
                crop_res = year_res['farm_profitability'][crop]
                graph_data['crop_yield'][crop].append({
                    'year': year,
                    'value': crop_res['yield_per_dunam']
                })
                graph_data['crop_profit'][crop].append({
                    'year': year,
                    'value': crop_res['profit']
                })
                graph_data['crop_profit_per_dunam'][crop].append({
                    'year': year,
                    'value': crop_res['profit'] / crop_res['area']
                })
            
            # Observed data
            if crop in year_res['observed']['actual_profits']:
                graph_data['observed_profit'][crop].append({
                    'year': year,
                    'value': year_res['observed']['actual_profits'][crop]
                })
    
    return graph_data

# Test the module if run directly
if __name__ == "__main__":
    print("=" * 50)
    print("TESTING run_model.py")
    print("=" * 50)
    
    # Run model for all years
    results = run_model_for_all_years()
    
    # Print summary
    print_model_results_summary(results)
    
    # Compare with observed
    compare_with_observed(results)
    
    # Prepare for graphs
    graph_data = get_results_for_graphs(results)
    print(f"\n✅ Data prepared for graphs: {len(graph_data['years'])} years")
    
    print("\n✅ Test complete!")
    print("\nNext step: Run plot_graphs.py to visualize these results")