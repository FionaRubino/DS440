from flask import Flask, jsonify, request
from flask_cors import CORS
from recommender import generate_combos_for_recipe, recommend_combinations

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/api/health")
def health():
    return {"status": "ok"}

@app.route("/api/recommend", methods=["POST"])
def recommend():
    data = request.json
    recipe_id = int(data.get("recipe_id", 0))  # ensure numeric

    # Handle budgets
    try:
        min_budget = float(data.get("min_budget", 0.0))
        max_budget = float(data.get("max_budget", float("inf")))
    except ValueError:
        return {"error": "min_budget and max_budget must be numbers"}, 400

    use_recipe_price = data.get("use_recipe_price", False)
    sort_by = data.get("sort_by", None)

    # Initialize filters dictionary
    user_filter = {}

    # Max stores filter
    filters = data.get("filters", {})           # <-- line to change
    max_stores = filters.get("num_stores")      # <-- line to change
    if max_stores is not None:
        try:
            max_stores = int(max_stores)        # <-- parse as int
        except ValueError:
            return {"error": "num_stores filter must be an integer"}, 400

    try:
        # Generate combos
        combos = generate_combos_for_recipe(recipe_id, min_budget, max_budget, use_recipe_price, max_stores=max_stores)

        # Rank and filter combos
        results = recommend_combinations(
            combos,
            store_penalty=2,
            user_sort=sort_by
        )

    except Exception as e:
        print("Backend error:", e)
        return {"error": str(e)}, 500

    # Format output
    output = [
        {
            "total_price": c.total_price,
            "recipe_price": c.recipe_price,
            "num_stores": c.num_stores,
            "adjusted_score": c.adjusted_score,
            "stores": c.store_assignments,
            "breakdown": c.breakdown
        }
        for c in results
    ]

    return jsonify({"recipe": recipe_id, "recommendations": output})

if __name__ == "__main__":
    app.run(debug=True, port=8000)