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
    recipe_id = data.get("recipe_id")
    min_budget = data.get("min_budget")
    max_budget = data.get("max_budget")
    sort_by = data.get("sort_by", None)
    filters = data.get("filters", None)

    # Call functions from recommender.py
    combos = generate_combos_for_recipe(recipe_id, min_budget, max_budget)
    results = recommend_combinations(
        combos,
        store_penalty=2,
        user_sort=sort_by,
        user_filter=filters
    )

    output = [
        {
            "total_price": c.total_price,
            "num_stores": c.num_stores,
            "adjusted_score": c.adjusted_score,
            "stores": c.store_assignments
        }
        for c in results
    ]

    return jsonify({"recipe": recipe_id, "recommendations": output})

if __name__ == "__main__":
    app.run(debug=True)