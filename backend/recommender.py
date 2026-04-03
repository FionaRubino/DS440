from itertools import product
from data_utils import load_recipes, load_prices

# -------------------------
# Load real data
# -------------------------
recipes = load_recipes("data/recipes.csv")
prices = load_prices("data/ingredients-total-cost-final.csv")


# -------------------------
# Combo Class
# -------------------------
class Combo:
    def __init__(self, store_assignments, total_price):
        self.store_assignments = store_assignments  # {ingredient: store}
        self.total_price = total_price
        self.num_stores = len(set(store_assignments.values()))
        self.adjusted_score = None


# -------------------------
# Generate Combinations
# -------------------------
def generate_combos_for_recipe(recipe_id, min_budget, max_budget):
    recipe = recipes.get(recipe_id)

    if not recipe:
        return []

    ingredients = recipe["ingredients"]

    # Build list of options for each ingredient
    options_per_ingredient = []
    for ing in ingredients:
        if ing not in prices:
            continue
        # Only include stores with valid prices
        options = [(store, price) for store, price in prices[ing].items() if price is not None]
        if not options:
            # If no valid price for ingredient, skip the recipe entirely
            return []
        options_per_ingredient.append(options)

    combos = []

    # Generate all combinations
    for combination in product(*options_per_ingredient):
        store_assignments = {}
        total_price = 0

        for ing, (store, price) in zip(ingredients, combination):
            store_assignments[ing] = store
            total_price += price

        # Keep only combos within budget
        if min_budget <= total_price <= max_budget:
            combos.append(Combo(store_assignments, total_price))

    return combos


# -------------------------
# Recommend / Rank Combos
# -------------------------
def recommend_combinations(combos, store_penalty=2, user_sort=None, user_filter=None):

    # Add adjusted score (penalize multiple stores)
    for combo in combos:
        combo.adjusted_score = combo.total_price + store_penalty * (combo.num_stores - 1)

    # Apply filters (example: max number of stores)
    if user_filter:
        for key, value in user_filter.items():
            combos = [c for c in combos if getattr(c, key) <= value]

    # Apply sorting
    if user_sort:
        combos.sort(key=lambda c: getattr(c, user_sort))
    else:
        combos.sort(key=lambda c: c.adjusted_score)

    return combos