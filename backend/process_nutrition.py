import pandas as pd
import numpy as np
import re

# 1. Load the original Excel sheets
nut_df = pd.read_excel('Ingredients_Nutrition.xlsx', sheet_name='Nutrition')
master_df = pd.read_excel('Ingredients_Nutrition.xlsx', sheet_name='Master')

# 2. Extract Servings from the Master Sheet
servings_dict = {}
for idx, row in master_df.iterrows():
    ing = str(row['Ingredient']).strip()
    if pd.isna(row['Quantity']) and ing != 'nan' and not ing.startswith('Totals') and not ing.startswith('Recipe Reference'):
        try:
            servings = float(row.iloc[-1]) 
            if not np.isnan(servings):
                servings_dict[ing] = servings
        except:
            pass

# 3. Helper function to remove "kcal", "g", "mg" from the cells
def clean_macro(val):
    if pd.isna(val): return None
    val = str(val).lower()
    val = re.sub(r'[a-z]', '', val).strip() # Deletes letters
    try:
        return float(val) if val else None
    except:
        return None

# Find the carb column dynamically
carb_col = [c for c in nut_df.columns if 'Carb' in c][0]

# 4. Map the serving size to every ingredient in the recipe
current_recipe = None
servings_list = []

for idx, row in nut_df.iterrows():
    ing = str(row['Ingredient']).strip()
    amount = row['Amount (Meal)']
    
    # Check if the row is a recipe header
    if pd.isna(amount) and ing != 'nan' and 'USDA:' not in ing and not ing.startswith('Totals') and not ing.startswith('Recipe Reference'):
        current_recipe = ing
        
    if current_recipe:
        servings_list.append(servings_dict.get(current_recipe, 1))
    else:
        servings_list.append(1)

nut_df['Recipe Servings'] = servings_list

# 5. Clean the macros into pure numbers
nut_df['Calories (Num)'] = nut_df['Calories'].apply(clean_macro)
nut_df['Fat (Num)'] = nut_df['Fat'].apply(clean_macro)
nut_df['Sodium (Num)'] = nut_df['Sodium'].apply(clean_macro)
nut_df['Carbs (Num)'] = nut_df[carb_col].apply(clean_macro)
nut_df['Protein (Num)'] = nut_df['Protein'].apply(clean_macro)

# 6. Create the exact Per-Serving Columns you asked for!
nut_df['Calories / Serving'] = nut_df['Calories (Num)'] / nut_df['Recipe Servings']
nut_df['Fat / Serving (g)'] = nut_df['Fat (Num)'] / nut_df['Recipe Servings']
nut_df['Sodium / Serving (mg)'] = nut_df['Sodium (Num)'] / nut_df['Recipe Servings']
nut_df['Carbs / Serving (g)'] = nut_df['Carbs (Num)'] / nut_df['Recipe Servings']
nut_df['Protein / Serving (g)'] = nut_df['Protein (Num)'] / nut_df['Recipe Servings']

# Clean up the temporary columns
nut_df = nut_df.drop(columns=['Calories (Num)', 'Fat (Num)', 'Sodium (Num)', 'Carbs (Num)', 'Protein (Num)'])

# 7. Save back to a new Excel file
nut_df.to_excel('Ingredients_Nutrition_UPDATED.xlsx', index=False)
print("Success! Your new Excel file is ready.")