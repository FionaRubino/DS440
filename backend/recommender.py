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
    def __init__(self, store_assignments, total_price, recipe_price):
        self.store_assignments = store_assignments  # {ingredient: store}
        self.total_price = total_price
        self.recipe_price = recipe_price
        self.num_stores = len(set(store_assignments.values()))
        self.adjusted_score = None


# -------------------------
# Generate Combinations
# -------------------------
def generate_combos_for_recipe(recipe_id, min_budget, max_budget,use_recipe_price=False):
    recipe = recipes.get(recipe_id)

    if not recipe:
        return []

    ingredients = recipe["ingredients"]

    # Build list of options
    options_per_ingredient = []
    for ing in ingredients:
        name = ing["name"]

        if name not in prices:
            continue

        options = [
            (store, data["price"], data["oz"])
            for store, data in prices[name].items()
            if data["price"] is not None and data["oz"] is not None
        ]

        if not options:
            return []

        options_per_ingredient.append(options)

    combos = []

    for combination in product(*options_per_ingredient):
        store_assignments = {}
        total_price = 0
        recipe_price = 0  # NEW

        for ing, (store, price, available_oz) in zip(ingredients, combination):
            name = ing["name"]
            required_oz = ing["required_oz"]

            store_assignments[name] = store

            # Existing total price (full purchase)
            total_price += price

            # NEW: proportional cost
            cost_per_oz = price / available_oz
            recipe_price += cost_per_oz * required_oz

        price_to_check = recipe_price if use_recipe_price else total_price

        if min_budget <= price_to_check <= max_budget:
            combos.append(Combo(store_assignments, total_price, recipe_price))

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