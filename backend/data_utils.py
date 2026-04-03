import csv

def load_recipes(file_path="data/recipes.csv"):
    recipes = {}
    with open(file_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            recipes[int(row["Recipe ID"])] = {
                "name": row["Recipe Name"],
                "ingredients": row["Ingredient List"].split(";")
            }
    return recipes


def load_prices(file_path="data/ingredients-total-cost-final.csv"):
    """
    Returns dict: prices[ingredient] = {store: price}
    Any non-numerical price is treated as None
    """
    prices = {}
    with open(file_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ing = row["Ingredient"]
            store = row["Store"]
            price_str = row["Price"].strip()

            try:
                price = float(price_str)
            except (ValueError, TypeError):
                price = None

            if ing not in prices:
                prices[ing] = {}
            prices[ing][store] = price
    return prices