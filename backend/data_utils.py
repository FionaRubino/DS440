import csv

def load_recipes(file_path="data/recipes.csv"):
    recipes = {}
    with open(file_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ingredients_raw = row["Ingredient List"].split(";")

            ingredients = []
            for item in ingredients_raw:
                name, oz = item.split("|")
                ingredients.append({
                    "name": name.strip(),
                    "required_oz": float(oz)
                })

            recipes[int(row["Recipe ID"])] = {
                "name": row["Recipe Name"],
                "ingredients": ingredients
            }

    return recipes


def load_prices(file_path="data/ingredients-total-cost-final.csv"):
    """
    Returns dict:
    prices[ingredient] = {
        store: {"price": float, "oz": float}
    }
    """
    prices = {}
    with open(file_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ing = row["Ingredient"]
            store = row["Store"]

            price_str = row["Price"].strip()
            oz_str = row["OZ"].strip()

            try:
                price = float(price_str)
                oz = float(oz_str)
            except (ValueError, TypeError):
                price = None
                oz = None

            if ing not in prices:
                prices[ing] = {}

            prices[ing][store] = {
                "price": price,
                "oz": oz
            }

    return prices