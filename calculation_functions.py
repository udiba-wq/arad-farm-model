"""
farm_model.py
Core model classes with all 14 functions from the flowchart
INPUT: Data from farm_data_loader.py
OUTPUT: Dictionary with all 14 function results
"""

class Expenses:
    """Represents farm-level fixed costs"""
    def __init__(self, admin_cost):
        self.admin_cost = admin_cost
    
    def get_admin_cost(self):
        """Return admin cost (used in Function 13)"""
        return self.admin_cost


class Crop:
    """
    Represents a single crop type
    Contains only constant parameters (A, B, thresholds, costs)
    """
    def __init__(self, crop_type, A, B, fixed_exp, est_costs, thresholds):
        self.crop_type = crop_type.lower()  # almond/vineyard/apricot
        self.A = A                          # Production function slope
        self.B = B                          # Production function intercept
        self.fixed_exp = fixed_exp          # Fixed expenses per dunam
        self.est_costs = est_costs          # Establishment costs per dunam
        self.thresholds = thresholds if thresholds else 0
        
        # Pre-calculate maximum yield
        self.max_yield = self.A * self.thresholds + self.B if self.thresholds > 0 else None
    
    # Function 1: Production Function
    def production_function(self, irrigation_m3_per_dunam):
        """
        Function 1: Production Function
        Input: irrigation amount (m³/dunam)
        Output: yield (kg/dunam)
        """
        if irrigation_m3_per_dunam <= self.thresholds:
            return max(0, self.A * irrigation_m3_per_dunam + self.B)
        else:
            return max(0, self.max_yield)
    
    # Function 2: Income Function Per Dunam
    def income_per_dunam_function(self, irrigation_m3_per_dunam, price_per_kg):
        """
        Function 2: Income Function Per Dunam
        Input: irrigation (m³/dunam), price (NIS/kg)
        Output: income per dunam (NIS/dunam)
        """
        yield_per_dunam = self.production_function(irrigation_m3_per_dunam)
        return yield_per_dunam * price_per_kg
    # Function 10: Crop Per Dunam Water Costs Function
    def water_cost_per_dunam_function(self, irrigation_m3_per_dunam, farm_water_price):
        """
        Function 10: Crop Per Dunam Water Costs Function
        Input: irrigation (m³/dunam), average farm water price (NIS/m³)
        Output: water cost per dunam (NIS/dunam)
        """
        return irrigation_m3_per_dunam * farm_water_price
    
    # Function 11: Fixed Costs Function (per dunam)
    def fixed_costs_per_dunam_function(self):
        """
        Function 11: Fixed Costs Function (per dunam)
        Output: total fixed costs per dunam (NIS/dunam)
        """
        return self.fixed_exp + self.est_costs


class Farm:
    """
    Represents the entire farm for a single year
    Contains variable data (areas, irrigation, prices) for that year
    """
    def __init__(self, crops, crop_data, water_params, admin_cost):
        """
        crops: list of Crop objects
        crop_data: dictionary with:
            - 'areas': {crop_type: dunam}
            - 'irrigations': {crop_type: m³/dunam}
            - 'prices': {crop_type: NIS/kg}
        water_params: dictionary with:
            - 'recycled_quota': m³
            - 'fresh_price': NIS/m³
            - 'recycled_price': NIS/m³
        admin_cost: NIS
        """
        self.crops = {crop.crop_type: crop for crop in crops}
        self.areas = crop_data['areas']
        self.irrigations = crop_data['irrigations']
        self.prices = crop_data['prices']
        self.recycled_quota = water_params['recycled_quota']
        self.fresh_price = water_params['fresh_price']
        self.recycled_price = water_params['recycled_price']
        self.admin_cost = admin_cost
        
        # Valid crop types present in this farm
        self.crop_types = list(self.areas.keys())
    
    # Helper: Get crop object by type
    def _get_crop(self, crop_type):
        """Get crop object for a given crop type"""
        return self.crops.get(crop_type)
    
    # Function 3: Income Area Function (per crop total income)
    def income_area_function(self):
        """
        Function 3: Income Area Function
        Output: dictionary {crop_type: total income from that crop (NIS)}
        """
        result = {}
        for crop_type in self.crop_types:
            crop = self._get_crop(crop_type)
            if crop:
                income_per_dunam = crop.income_per_dunam_function(
                    self.irrigations[crop_type], 
                    self.prices[crop_type]
                )
                result[crop_type] = income_per_dunam * self.areas[crop_type]
        return result
    
    # Function 4: Farm Income Function
    def farm_income_function(self):
        """
        Function 4: Farm Income Function
        Output: total farm income (NIS)
        """
        return sum(self.income_area_function().values())
    
    # Function 5: Irrigation Area Function (total water per crop)
    def irrigation_area_function(self):
        """
        Function 5: Irrigation Area Function
        Output: dictionary {crop_type: total water for that crop (m³)}
        """
        result = {}
        for crop_type in self.crop_types:
            result[crop_type] = self.areas[crop_type] * self.irrigations[crop_type]
        return result
    
    # Function 6: Total Irrigation Function
    def total_irrigation_function(self):
        """
        Function 6: Total Irrigation Function
        Output: total farm water use (m³)
        """
        return sum(self.irrigation_area_function().values())
    
    # Function 7: Freshwater Function
    def freshwater_function(self):
        """
        Function 7: Freshwater Function
        Output: amount of freshwater needed (m³)
        """
        total_water = self.total_irrigation_function()
        return max(0, total_water - self.recycled_quota)
    
    # Helper: Recycled water used
    def _recycled_water_used(self):
        """Helper: amount of recycled water actually used (m³)"""
        total_water = self.total_irrigation_function()
        return min(total_water, self.recycled_quota)
    
    # Function 8: Water Price Function
    def water_price_function(self):
        """
        Function 8: Water Price Function
        Output: total water cost (NIS)
        """
        total_water = self.total_irrigation_function()
        if total_water == 0:
            return 0
        
        freshwater = self.freshwater_function()
        recycled_used = self._recycled_water_used()
        
        return (freshwater * self.fresh_price) + (recycled_used * self.recycled_price)
    
    # Function 9: Farm Water Price (average)
    def farm_water_price_function(self):
        """
        Function 9: Farm Water Price (average per m³)
        Output: average water price (NIS/m³)
        """
        total_water = self.total_irrigation_function()
        if total_water == 0:
            return 0
        return self.water_price_function() / total_water
    
    # Function 10 is in Crop class (water_cost_per_dunam_function)
    
    # Function 11 is in Crop class (fixed_costs_per_dunam_function)
    
    # Function 12: Farm Fixed Costs Function
    def farm_fixed_costs_function(self):
        """
        Function 12: Farm Fixed Costs Function
        Output: total fixed costs for all crops (NIS)
        """
        total = 0
        for crop_type in self.crop_types:
            crop = self._get_crop(crop_type)
            if crop:
                total += self.areas[crop_type] * crop.fixed_costs_per_dunam_function()
        return total
    
    # Function 13: Total Costs Function
    def total_costs_function(self):
        """
        Function 13: Total Costs Function
        Output: dictionary with cost breakdown
        """
        crop_fixed = self.farm_fixed_costs_function()
        water_cost = self.water_price_function()
        admin = self.admin_cost
        
        return {
            'crop_fixed_costs': crop_fixed,
            'water_costs': water_cost,
            'admin_costs': admin,
            'total': crop_fixed + water_cost + admin
        }
    
    # Function 14: Farm Profitability Function
    def farm_profitability_function(self):
        """
        Function 14: Farm Profitability Function
        Output: dictionary with profit details for each crop
        """
        farm_water_price = self.farm_water_price_function()
        result = {}
        
        for crop_type in self.crop_types:
            crop = self._get_crop(crop_type)
            if not crop:
                continue
                
            area = self.areas[crop_type]
            irrigation = self.irrigations[crop_type]
            price = self.prices[crop_type]
            
            # Income
            income_per_dunam = crop.income_per_dunam_function(irrigation, price)
            total_income = income_per_dunam * area
            
            # Costs
            fixed_costs = area * crop.fixed_costs_per_dunam_function()
            water_costs = area * crop.water_cost_per_dunam_function(irrigation, farm_water_price)
            total_costs = fixed_costs + water_costs
            
            result[crop_type] = {
                'income': total_income,
                'costs': total_costs,
                'profit': total_income - total_costs,
                'area': area,
                'irrigation_per_dunam': irrigation,
                'yield_per_dunam': crop.production_function(irrigation),
                'income_per_dunam': income_per_dunam
            }
        
        return result
    
    # Helper: Get all results in one dictionary
    def get_all_results(self):
        """
        Return all 14 function outputs in one dictionary
        This matches the flowchart outputs
        """
        crop_profits = self.farm_profitability_function()
        
        return {
            # Function 1: Production Function (yield per crop)
            'production_function': {c: p['yield_per_dunam'] for c, p in crop_profits.items()},
            
            # Function 2: Income Per Dunam
            'income_per_dunam': {c: p['income_per_dunam'] for c, p in crop_profits.items()},
            
            # Function 3: Income Area Function (total crop income)
            'income_area': self.income_area_function(),
            
            # Function 4: Farm Income Function
            'farm_income': self.farm_income_function(),
            
            # Function 5: Irrigation Area Function (total water per crop)
            'irrigation_area': self.irrigation_area_function(),
            
            # Function 6: Total Irrigation Function
            'total_irrigation': self.total_irrigation_function(),
            
            # Function 7: Freshwater Function
            'freshwater': self.freshwater_function(),
            
            # Function 8: Water Price Function (total cost)
            'water_price_total': self.water_price_function(),
            
            # Function 9: Farm Water Price (average)
            'farm_water_price': self.farm_water_price_function(),
            
            # Function 10: Crop Per Dunam Water Costs
            'crop_water_cost_per_dunam': {
                c: p['costs']/p['area'] - (self.farm_fixed_costs_function()/p['area'] if p['area'] > 0 else 0)
                for c, p in crop_profits.items()
            },
            
            # Function 11: Fixed Costs Function (per crop total)
            'fixed_costs': {
                c: p['area'] * self._get_crop(c).fixed_costs_per_dunam_function()
                for c, p in crop_profits.items() if self._get_crop(c)
            },
            
            # Function 12: Farm Fixed Costs Function
            'farm_fixed_costs': self.farm_fixed_costs_function(),
            
            # Function 13: Total Costs Function
            'total_costs': self.total_costs_function(),
            
            # Function 14: Farm Profitability Function
            'farm_profitability': crop_profits,
            
            # Also include farm total profit (derived from function 14)
            'farm_total_profit': sum(p['profit'] for p in crop_profits.values())
        }


# Quick test if run directly
if __name__ == "__main__":
    print("=" * 50)
    print("TESTING farm_model.py")
    print("=" * 50)
    
    # Create a test crop
    test_crop = Crop("almond", 0.25, 40, 1200, 800, 1000)
    
    print("\nTesting Crop class:")
    print(f"  Crop type: {test_crop.crop_type}")
    print(f"  Production at 800 m³: {test_crop.production_function(800):.1f} kg/dunam")
    print(f"  Production at 1200 m³: {test_crop.production_function(1200):.1f} kg/dunam")
    print(f"  Income per dunam at 800 m³, price 18: {test_crop.income_per_dunam_function(800, 18):.0f} NIS")
    print(f"  Fixed costs per dunam: {test_crop.fixed_costs_per_dunam_function()} NIS")
    
    print("\n✅ Test complete!")
