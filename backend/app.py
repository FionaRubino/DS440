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
    recipe_id = int(data.get("recipe_id"))  # ensure numeric
    try:
        min_budget = float(data.get("min_budget")) if data.get("min_budget") else 0.0
        max_budget = float(data.get("max_budget")) if data.get("max_budget") else float('inf')
    except ValueError:
        return {"error": "min_budget and max_budget must be numbers"}, 400

    sort_by = data.get("sort_by", None)
    filters = data.get("filters", None)

    try:
        combos = generate_combos_for_recipe(recipe_id, min_budget, max_budget)
        results = recommend_combinations(
            combos,
            store_penalty=2,
            user_sort=sort_by,
            user_filter=filters
        )
    except Exception as e:
        print("Backend error:", e)
        return {"error": str(e)}, 500

    output = [
    {
        "total_price": c.total_price,
        "recipe_price": c.recipe_price,  # NEW
        "num_stores": c.num_stores,
        "adjusted_score": c.adjusted_score,
        "stores": c.store_assignments
    }
    for c in results
    ]

    return jsonify({"recipe": recipe_id, "recommendations": output})

if __name__ == "__main__":
    app.run(debug=True, port=8000)