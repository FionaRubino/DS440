from itertools import product
from data_utils import load_recipes, load_prices
from heapq import nsmallest

# -------------------------
# Load real data
# -------------------------
recipes = load_recipes("data/recipes.csv")
prices = load_prices("data/ingredients-total-cost-final.csv")

# -------------------------
# Combo Class
# -------------------------
class Combo:
    def __init__(self, store_assignments, total_price, recipe_price, breakdown):
        self.store_assignments = store_assignments  # {ingredient: store}
        self.total_price = total_price
        self.recipe_price = recipe_price
        self.breakdown = breakdown
        self.num_stores = len(set(store_assignments.values()))
        self.adjusted_score = None


# -------------------------
# Generate Combinations
# -------------------------

def generate_combos_for_recipe(
    recipe_id,
    min_budget,
    max_budget,
    use_recipe_price=False,
    top_stores_per_ingredient=6,
    max_results=10,
    max_stores=None,  # NEW: limit number of stores
):
    recipe = recipes.get(recipe_id)
    if not recipe:
        return []

    ingredients = recipe["ingredients"]
    options_per_ingredient = []

    # Build options for each ingredient
    for ing in ingredients:
        name = ing["name"]
        required_oz = ing["required_oz"]

        if name not in prices:
            continue

        # List of tuples: (store, price, oz)
        all_options = [
            (store, data["price"], data["oz"])
            for store, data in prices[name].items()
            if data["price"] is not None and data["oz"] is not None
        ]

        if not all_options:
            return []

        # Calculate proportional cost if recipe price toggle is on
        if use_recipe_price:
            all_options = [
                (store, price, oz, price / oz * required_oz)
                for store, price, oz in all_options
            ]
            top_options = nsmallest(top_stores_per_ingredient, all_options, key=lambda x: x[3])
            options_per_ingredient.append([(s, p, oz) for s, p, oz, _ in top_options])
        else:
            top_options = nsmallest(top_stores_per_ingredient, all_options, key=lambda x: x[1])
            options_per_ingredient.append(top_options)

    combos = []

    # Generate all combinations with early store filtering
    for combination in product(*options_per_ingredient):
        store_assignments = {}
        total_price = 0
        recipe_price = 0
        ingredient_breakdown = []

        for ing, (store, price, available_oz) in zip(ingredients, combination):
            store_assignments[ing["name"]] = store
            total_price += price
            cost_per_oz = price / available_oz
            used_cost = round(cost_per_oz * ing["required_oz"], 2)
            recipe_price += used_cost
            ingredient_breakdown.append({
                "ingredient": ing["name"],
                "store": store,
                "total_item_price": price,
                "used_cost": used_cost,
                "required_oz": ing["required_oz"],
                "available_oz": available_oz
            })

        recipe_price = round(recipe_price, 2)

        # EARLY SKIP: too many stores
        unique_stores = set(store_assignments.values())
        if max_stores is not None and len(unique_stores) > max_stores:
            continue

        # Skip if combo outside budget
        price_to_check = recipe_price if use_recipe_price else total_price
        if not (min_budget <= price_to_check <= max_budget):
            continue

        combos.append(Combo(store_assignments, total_price, recipe_price, ingredient_breakdown))

        # Stop early if we reach max_results
        if len(combos) >= max_results:
            break

    return combos


# -------------------------
# Recommend / Rank Combos
# -------------------------
def recommend_combinations(combos, store_penalty=2, user_sort=None, user_filter=None, top_results=10):
    # Penalize multiple stores for adjusted score
    for combo in combos:
        combo.adjusted_score = combo.total_price + store_penalty * (combo.num_stores - 1)

    print("Remaining combos after filter:", len(combos))

    # Apply sorting
    if user_sort:
        combos.sort(key=lambda c: getattr(c, user_sort))
    else:
        combos.sort(key=lambda c: c.adjusted_score)

    return combos[:top_results]  # Return only top N