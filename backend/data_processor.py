import pandas as pd
import numpy as np
import re

# --- CHANGED: Read directly from the Excel file sheets ---
# Note: You may need to run `pip install openpyxl` in your terminal if you don't have it installed
nut_df = pd.read_excel('Ingredients_Nutrition.xlsx', sheet_name='Nutrition')
master_df = pd.read_excel('Ingredients_Nutrition.xlsx', sheet_name='Master')

# 2. Extract Servings from the Master Sheet
servings_dict = {}
for idx, row in master_df.iterrows():
    ing = str(row['Ingredient']).strip()
    if pd.isna(row['Quantity']) and ing != 'nan' and not ing.startswith('Totals') and not ing.startswith('Recipe Reference'):
        try:
            # The serving size is in the last column
            servings = float(row.iloc[-1]) 
            if not np.isnan(servings):
                servings_dict[ing] = servings
        except:
            pass

# Helper function to clean macro strings (removes 'g', 'kcal', 'mg')
def clean_macro(val):
    if pd.isna(val): return 0.0
    val = str(val).lower()
    val = re.sub(r'[a-z]', '', val).strip()
    try:
        return float(val) if val else 0.0
    except:
        return 0.0

# 3. Aggregate Total Macros per Recipe
recipes = []
current_recipe = None

# Dynamically find the Carbs column (sometimes has a trailing space)
carb_col = [c for c in nut_df.columns if 'Carb' in c][0]
current_macros = {'Calories': 0, 'Fat': 0, 'Sodium': 0, 'Carbs': 0, 'Protein': 0}

for idx, row in nut_df.iterrows():
    ing = str(row['Ingredient']).strip()
    amount = row['Amount (Meal)']
    
    # Identify recipe headers
    if pd.isna(amount) and ing != 'nan' and 'USDA:' not in ing and not ing.startswith('Totals') and not ing.startswith('Recipe Reference'):
        if current_recipe:
            recipes.append({
                'Recipe': current_recipe,
                'Total Calories': current_macros['Calories'],
                'Total Fat': current_macros['Fat'],
                'Total Sodium': current_macros['Sodium'],
                'Total Carbs': current_macros['Carbs'],
                'Total Protein': current_macros['Protein']
            })
        current_recipe = ing
        current_macros = {'Calories': 0, 'Fat': 0, 'Sodium': 0, 'Carbs': 0, 'Protein': 0}
        
    # Aggregate ingredients
    elif not pd.isna(amount) and ing != 'nan':
        current_macros['Calories'] += clean_macro(row['Calories'])
        current_macros['Fat'] += clean_macro(row['Fat'])
        current_macros['Sodium'] += clean_macro(row['Sodium'])
        current_macros['Carbs'] += clean_macro(row[carb_col])
        current_macros['Protein'] += clean_macro(row['Protein'])

# Add the final recipe
if current_recipe:
    recipes.append({
        'Recipe': current_recipe,
        'Total Calories': current_macros['Calories'],
        'Total Fat': current_macros['Fat'],
        'Total Sodium': current_macros['Sodium'],
        'Total Carbs': current_macros['Carbs'],
        'Total Protein': current_macros['Protein']
    })

df = pd.DataFrame(recipes)

# 4. Calculate Per-Serving Macros
for macro in ['Calories', 'Fat', 'Sodium', 'Carbs', 'Protein']:
    df[macro] = df.apply(lambda r: r[f'Total {macro}'] / servings_dict.get(r['Recipe'], 1), axis=1)

# Clean up recipe names for cleaner output
df['Recipe'] = df['Recipe'].apply(lambda x: x.split('-')[0].strip())
df = df[~df['Recipe'].str.contains("Recipe reference|Recipe:", na=False, case=False, regex=True)].copy()

# 5. Define the 10 Custom Nutritional Score Profiles
df['1. General Wellness'] = 100 - (df['Calories']/2000*20) - (df['Sodium']/2300*30) - (df['Fat']/78*15) - (df['Carbs']/275*10) + (df['Protein']/50*25)
df['2. Muscle Building'] = 100 - (df['Calories']/2500*10) - (df['Sodium']/2300*15) - (df['Fat']/78*10) + (df['Carbs']/300*10) + (df['Protein']/150*50)
df['3. Fat Loss'] = 100 - (df['Calories']/1500*40) - (df['Sodium']/2300*15) - (df['Fat']/60*20) - (df['Carbs']/150*15) + (df['Protein']/100*30)
df['4. Endurance Athlete'] = 100 - (df['Calories']/3000*5) - (df['Sodium']/2500*10) - (df['Fat']/80*15) + (df['Carbs']/350*40) + (df['Protein']/100*20)
df['5. Keto / Low Carb'] = 100 - (df['Calories']/2000*10) - (df['Sodium']/2300*10) + (df['Fat']/150*20) - (df['Carbs']/30*50) + (df['Protein']/100*20)
df['6. Brain Health'] = 100 - (df['Calories']/2000*20) - (df['Sodium']/2300*10) - (df['Carbs']/100*30) + (df['Fat']/70*20) + (df['Protein']/100*20)
df['7. Hangover Recovery'] = 100 + (df['Calories']/2500*10) + (df['Sodium']/2300*30) + (df['Carbs']/300*20) - (df['Fat']/80*10) + (df['Protein']/50*10)
df['8. High Satiety'] = 100 - (df['Calories']/1500*30) - (df['Carbs']/200*20) + (df['Fat']/70*20) + (df['Protein']/100*50)
df['9. Heart Healthy'] = 100 - (df['Calories']/2000*20) - (df['Sodium']/1500*40) - (df['Fat']/60*20) - (df['Carbs']/250*10) + (df['Protein']/50*20)
df['10. Lean Body Recomp'] = 100 - (df['Calories']/2000*20) - (df['Sodium']/2300*10) - (df['Fat']/60*10) + (df['Carbs']/200*10) + (df['Protein']/150*40)

# 6. Export full results to JSON (for your web app)
df.to_json('Young_Adult_Nutrition_Leaderboards.json', orient='records', indent=4)
print("Successfully generated JSON from the Excel file!")