import os

dep_path = "assets/depreciation.py"
os.makedirs("assets", exist_ok=True)

depreciation_service = """
from datetime import datetime

def calculate_vehicle_depreciation(purchase_price, acquisition_year, annual_depreciation_rate=0.15):
    \"\"\"
    Estimates current market value based on make, model, and year of acquisition[cite: 1].
    \"\"\"
    current_year = datetime.now().year
    age = current_year - acquisition_year
    
    if age <= 0:
        return purchase_price
        
    # Compound depreciation formula
    depreciated_value = purchase_price * ((1 - annual_depreciation_rate) ** age)
    return max(round(depreciated_value, 2), 500.00) # Floor minimum salvage value
"""

with open(dep_path, "w", encoding="utf-8") as f:
    f.write(depreciation_service)

print("SUCCESS: Vehicle Depreciation Calculator algorithm service created successfully!")
