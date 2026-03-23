import pandas as pd
import re
import json

def clean_val(val):
    """Removes text units (g, mg, kcal) and cleans numeric strings."""
    if pd.isna(val) or str(val).strip() == '' or 'Repeat' in str(val):
        return 0.0
    val = str(val).replace('`', '').replace(',', '').strip()
    match = re.search(r"(\d+\.?\d*)", val)
    return float(match.group(1)) if match else 0.0

def calculate_score(row):
    """Calculates the NutriScore (0-100)."""
    cal = row['Calories']
    if cal <= 0: return 0.0
    
    # Protein Bonus: +1.5 points per 1% of protein calories
    p_perc = (row['Protein'] * 4 / cal) * 100
    p_bonus = p_perc * 1.5
    
    # Sodium Penalty: -15 points per 1mg per calorie
    s_penalty = (row['Sodium'] / cal) * 15
    
    # Fat Penalty: -1 point per 1% over 35% fat calories
    f_perc = (row['Fat'] * 9 / cal) * 100
    f_penalty = max(0, f_perc - 35)
    
    # Carb Penalty: -1 point per 1% over 60% carb calories
    c_perc = (row['Carbs'] * 4 / cal) * 100
    c_penalty = max(0, c_perc - 60)
    
    score = 60 + p_bonus - s_penalty - f_penalty - c_penalty
    return round(max(0, min(100, score)), 1)

# Load data
df = pd.read_excel('Ingredients_Nutrition.xlsx'
                   , sheet_name='Nutrition', engine='openpyxl')
df.columns = [c.strip() for c in df.columns]

recipes = []
current_recipe = None
totals = {'Calories': 0, 'Fat': 0, 'Sodium': 0, 'Carbs': 0, 'Protein': 0}

for i, row in df.iterrows():
    name = str(row['Ingredient'])
    if '-' in name and 'USDA' not in name and 'Total' not in name:
        current_recipe = name
        totals = {k: 0 for k in totals}
        continue
    
    if 'Totals/Meal Total' in name and current_recipe:
        # Final recipe data capture
        r_data = {'Recipe': current_recipe, **totals}
        
        # Override for missing Meatloaf/Burrito data calculated manually
        if 'Meatloaf' in current_recipe and r_data['Calories'] == 0:
            r_data.update({'Calories': 1822, 'Fat': 117, 'Sodium': 3523, 'Carbs': 86.5, 'Protein': 101})
        if 'Burrito' in current_recipe and r_data['Calories'] == 0:
            r_data.update({'Calories': 2667, 'Fat': 170.5, 'Sodium': 2830, 'Carbs': 176, 'Protein': 101})
            
        r_data['NutriScore'] = calculate_score(pd.Series(r_data))
        recipes.append(r_data)
        continue
    
    if current_recipe:
        totals['Calories'] += clean_val(row['Calories'])
        totals['Fat'] += clean_val(row['Fat'])
        totals['Sodium'] += clean_val(row['Sodium'])
        totals['Carbs'] += clean_val(row.get('Carbs ', row.get('Carbs', 0)))
        totals['Protein'] += clean_val(row['Protein'])

# Export to JSON for your Web App
pd.DataFrame(recipes).to_json('recipes_data.json', orient='records', indent=4)
print("Data processed and saved to recipes_data.json")
